# 🚨 PROBLEMA REAL ENCONTRADO - get_facts() NO FUNCIONA

## ⚡ EL PROBLEMA VERDADERO

**EL FRAMEWORK GUARDA CON `session_id` COMO HASH KEY PERO BUSCA CON `user_id`**

---

## 🔍 CÓDIGO PROBLEMÁTICO EN EL FRAMEWORK

### GUARDAR (save_fact) - USA session_id:
```python
async def save_fact(self, user_id: str, category: str, key: str, value: Any, **kwargs) -> bool:
    key_values = self._generate_key_values(user_id, category, key, "FACT")
    
    item = {
        **key_values,
        'user_id': user_id,
        'session_id': kwargs.get('session_id', user_id),  # ← GUARDA session_id
        'category': category,
        'key': key,
        'value': value,
        ...
    }
    
    self.table.put_item(Item=item)
```

### RECUPERAR (get_facts) - BUSCA CON user_id:
```python
async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    response = self.table.scan(
        FilterExpression=f'user_id = :user_id AND begins_with({self.range_key_name}, :fact_prefix)',
        #                    ^^^^^^^ BUSCA POR user_id
        ExpressionAttributeValues={
            ':user_id': user_id,  # ← BUSCA por user_id
            ':fact_prefix': 'FACT#'
        }
    )
```

---

## 🎯 EL PROBLEMA

### 1. La tabla tiene schema:
```
Hash Key (Partition Key): session_id
Range Key (Sort Key): timestamp  
```

### 2. save_fact() guarda:
```json
{
  "session_id": "test-123",          ← HASH KEY (lo que DynamoDB usa para particionar)
  "timestamp": "FACT#test#my_key",   ← RANGE KEY
  "user_id": "test-123",              ← Campo adicional (NO es key)
  "key": "my_key",
  "value": "my_value"
}
```

### 3. get_facts() busca:
```python
FilterExpression='user_id = :user_id AND begins_with(timestamp, :fact_prefix)'
```

**PROBLEMA**: 
- DynamoDB hace SCAN completo de la tabla
- Filtra por `user_id = :user_id` (campo que NO es hash key)
- NO usa el índice de la tabla eficientemente
- Si `user_id` NO coincide exactamente, NO encuentra nada

---

## 🔬 POR QUÉ NO FUNCIONA

### Escenario del equipo de API:

```python
# El API llama:
await client_v11.save_fact(
    user_id="test-123",      # Se usa como session_id
    category="test",
    key="my_key",
    value="my_value"
)

# Guarda en DynamoDB:
{
  "session_id": "test-123",     # ← Hash Key
  "timestamp": "FACT#test#my_key",
  "user_id": "test-123",        # ← Campo adicional
  ...
}

# Luego llama:
facts = await client_v11.get_facts("test-123")

# Busca con:
FilterExpression='user_id = :user_id AND begins_with(timestamp, :fact_prefix)'
# Con user_id = "test-123"

# ✅ DEBERÍA funcionar si user_id == session_id
```

**PERO...**

Si hay CUALQUIER discrepancia entre `user_id` y `session_id`, NO encuentra nada.

---

## 🔧 LA SOLUCIÓN CORRECTA

El framework debe buscar usando el HASH KEY de la tabla, no un campo adicional.

### OPCIÓN 1: Buscar por session_id (si user_id == session_id):

```python
async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    # ✅ CORRECTO: Usar el hash_key de la tabla
    response = self.table.query(  # ← QUERY en lugar de SCAN
        KeyConditionExpression=Key(self.hash_key_name).eq(user_id) & 
                              Key(self.range_key_name).begins_with('FACT#')
    )
```

### OPCIÓN 2: Agregar user_id como hash_key en la tabla:

Si la tabla debe buscar por `user_id`, entonces la tabla debe tener:
```
Hash Key: user_id
Range Key: timestamp
```

Y guardar así:
```json
{
  "user_id": "user123",           ← HASH KEY
  "timestamp": "FACT#test#key",   ← RANGE KEY
  "session_id": "session456",     ← Campo adicional
  ...
}
```

---

## 🎯 EL PROBLEMA CON `_generate_key_values()`

```python
def _generate_key_values(self, user_id: str, category: str, key: str, item_type: str):
    # Common patterns for different schema types
    if self.hash_key_name in ['session_id', 'id', 'pk']:
        # Simple session-based schema
        hash_value = user_id  # ← USA user_id como hash_value
        range_value = f"{item_type}#{category}#{key}"
    ...
    
    return {
        self.hash_key_name: hash_value,  # ← Se guarda user_id en el campo hash_key
        self.range_key_name: range_value
    }
```

**PROBLEMA**:
- Si `hash_key_name` = 'session_id'
- Entonces guarda `{'session_id': user_id}`
- Pero luego busca con `FilterExpression='user_id = :user_id'`
- **NO coinciden los campos**

---

## ✅ SOLUCIÓN DEFINITIVA

### FIX 1: Hacer que get_facts() use el hash_key correcto:

```python
async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        # ✅ USAR QUERY en lugar de SCAN
        # ✅ USAR hash_key_name en lugar de 'user_id'
        
        if category:
            response = self.table.query(
                KeyConditionExpression=(
                    Key(self.hash_key_name).eq(user_id) &
                    Key(self.range_key_name).begins_with(f'FACT#{category}#')
                )
            )
        else:
            response = self.table.query(
                KeyConditionExpression=(
                    Key(self.hash_key_name).eq(user_id) &
                    Key(self.range_key_name).begins_with('FACT#')
                )
            )
        
        # Convertir items
        facts = []
        for item in response.get('Items', []):
            fact = {
                'key': item.get('key', ''),
                'value': item.get('value', ''),
                'category': item.get('category', ''),
                'confidence': float(item.get('confidence', 0.0)),
                'created_at': item.get('created_at', ''),
                'updated_at': item.get('updated_at', '')
            }
            facts.append(fact)
        
        return facts
        
    except Exception as e:
        logger.error(f"Error getting facts: {e}")
        return []
```

---

## 📊 COMPARACIÓN

### CÓDIGO ACTUAL (ROTO):
```python
# ❌ USA SCAN (lento e ineficiente)
# ❌ BUSCA por 'user_id' (campo que no es key)
response = self.table.scan(
    FilterExpression=f'user_id = :user_id AND begins_with({self.range_key_name}, :fact_prefix)',
    ExpressionAttributeValues={
        ':user_id': user_id,
        ':fact_prefix': 'FACT#'
    }
)
```

### CÓDIGO CORREGIDO:
```python
# ✅ USA QUERY (rápido y eficiente)
# ✅ BUSCA por hash_key_name (el campo correcto)
response = self.table.query(
    KeyConditionExpression=(
        Key(self.hash_key_name).eq(user_id) &
        Key(self.range_key_name).begins_with('FACT#')
    )
)
```

---

## 🚨 IMPACTO

### Performance:
- **ANTES**: SCAN completo de tabla (lento, caro)
- **DESPUÉS**: QUERY con índice (rápido, barato)

### Funcionalidad:
- **ANTES**: NO encuentra facts (busca en campo incorrecto)
- **DESPUÉS**: Encuentra todos los facts (busca en hash_key correcto)

### Costos:
- **ANTES**: Alto (SCAN de toda la tabla)
- **DESPUÉS**: Bajo (QUERY solo la partición necesaria)

---

## ✅ RESUMEN

**EL PROBLEMA REAL**:
1. La tabla tiene `session_id` como Hash Key
2. save_fact() guarda usando `session_id`
3. get_facts() busca usando `user_id` (campo que NO es key)
4. **Result**: NO encuentra los facts

**LA SOLUCIÓN**:
1. Cambiar get_facts() para usar QUERY en lugar de SCAN
2. Usar `self.hash_key_name` en lugar de hardcodear 'user_id'
3. Usar KeyConditionExpression en lugar de FilterExpression

**CÓDIGO FIX**:
```python
response = self.table.query(
    KeyConditionExpression=(
        Key(self.hash_key_name).eq(user_id) &
        Key(self.range_key_name).begins_with('FACT#')
    )
)
```

---

**ESTO ES EL PROBLEMA REAL. No es el tema de `#range_key` vs f-string. El problema es que usa SCAN con FilterExpression en lugar de QUERY con KeyConditionExpression.**
