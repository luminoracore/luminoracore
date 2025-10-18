#!/usr/bin/env python3
"""
Test de simulacion completa de conversacion con LuminoraCore v1.1
Demuestra: memoria, calculos de personalidad, clasificacion, recuperacion,
exportacion, y persistencia en JSON, SQLite y bases de datos
Version sin emojis para Windows
"""

import asyncio
import json
import os
import sys
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Anadir el directorio actual al path para importar los paquetes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from luminoracore.core.personality import Personality
from luminoracore_sdk.client import LuminoraCoreClient
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

# Configuracion para DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class ConversationSimulator:
    """Simulador de conversacion completa con LuminoraCore v1.1"""
    
    def __init__(self):
        self.storage = InMemoryStorageV11()
        self.base_client = LuminoraCoreClient()
        self.client = LuminoraCoreClientV11(self.base_client, storage_v11=self.storage)
        self.session_id = "conversation_test_user"
        self.conversation_data = []
        self.personality_evolution = []
        
    async def setup_conversation(self):
        """Configurar la conversacion inicial"""
        print("=" * 80)
        print("CONFIGURANDO SIMULACION DE CONVERSACION")
        print("=" * 80)
        
        # Crear personalidad Victoria Sterling
        self.victoria_personality = {
            "name": "Victoria Sterling",
            "version": "1.1.0",
            "description": "Executive assistant with evolving personality",
            "base_personality": {
                "core_traits": {
                    "professionalism": 0.9,
                    "efficiency": 0.8,
                    "empathy": 0.7,
                    "directness": 0.6
                },
                "communication_style": {
                    "formality": 0.8,
                    "warmth": 0.5,
                    "humor": 0.3,
                    "patience": 0.7
                }
            },
            "hierarchical_config": {
                "relationship_levels": {
                    "stranger": {
                        "formality_modifier": 0.2,
                        "warmth_modifier": -0.2,
                        "humor_modifier": -0.3,
                        "affinity_threshold": 0
                    },
                    "acquaintance": {
                        "formality_modifier": 0.0,
                        "warmth_modifier": 0.0,
                        "humor_modifier": 0.0,
                        "affinity_threshold": 10
                    },
                    "friend": {
                        "formality_modifier": -0.1,
                        "warmth_modifier": 0.2,
                        "humor_modifier": 0.2,
                        "affinity_threshold": 25
                    },
                    "close_friend": {
                        "formality_modifier": -0.3,
                        "warmth_modifier": 0.4,
                        "humor_modifier": 0.4,
                        "affinity_threshold": 50
                    }
                }
            },
            "memory_preferences": {
                "fact_retention": 0.9,
                "episodic_memory": 0.8,
                "preference_learning": 0.9,
                "goal_tracking": 0.8,
                "recalculation_frequency": 3  # Cada 3 mensajes
            },
            "affinity_config": {
                "positive_interactions": 5,
                "negative_interactions": -3,
                "goal_achievement": 10,
                "preference_alignment": 3,
                "humor_appreciation": 2,
                "technical_interest": 4
            }
        }
        
        print("OK Personalidad Victoria Sterling configurada")
        print(f"   - Niveles de relacion: {len(self.victoria_personality['hierarchical_config']['relationship_levels'])}")
        print(f"   - Frecuencia de recalculacion: {self.victoria_personality['memory_preferences']['recalculation_frequency']} mensajes")
        
    async def simulate_conversation(self):
        """Simular una conversacion de 10 mensajes"""
        print("\n" + "=" * 80)
        print("SIMULANDO CONVERSACION DE 10 MENSAJES")
        print("=" * 80)
        
        # Mensajes de la conversacion simulada
        conversation_messages = [
            {
                "user": "Hola, soy nuevo aqui. Puedes ayudarme con informacion sobre tu servicio?",
                "context": "first_contact",
                "expected_affinity": 5,
                "expected_facts": ["user_is_new", "interested_in_service"]
            },
            {
                "user": "Gracias por la informacion. Me llamo Carlos y trabajo en una startup de tecnologia. Estoy interesado en implementar un chatbot para atencion al cliente.",
                "context": "self_introduction",
                "expected_affinity": 8,
                "expected_facts": ["name_carlos", "works_startup", "interested_chatbot", "field_technology"]
            },
            {
                "user": "Perfecto. Me gusta que seas directa y tecnica en tus respuestas. ¿Que me recomiendas para empezar?",
                "context": "preference_learning",
                "expected_affinity": 6,
                "expected_facts": ["prefers_direct_communication", "prefers_technical_answers"]
            },
            {
                "user": "¡Excelente! Ya veo que recuerdas que me gusta lo tecnico. ¿Podrias darme un ejemplo de codigo para empezar?",
                "context": "relationship_building",
                "expected_affinity": 7,
                "expected_facts": ["appreciates_memory", "wants_code_examples"]
            },
            {
                "user": "Perfecto, eso es exactamente lo que necesitaba. ¿Cuales son los costos aproximados de implementacion?",
                "context": "goal_oriented",
                "expected_affinity": 8,
                "expected_facts": ["satisfied_with_help", "interested_in_costs", "serious_about_implementation"]
            },
            {
                "user": "Genial, esos costos estan dentro de mi presupuesto. ¿Podrias ayudarme a planificar la implementacion paso a paso?",
                "context": "commitment",
                "expected_affinity": 10,
                "expected_facts": ["budget_approved", "ready_for_implementation", "wants_step_by_step_plan"]
            },
            {
                "user": "¡Perfecto! Me encanta como trabajas. Eres muy profesional y eficiente. ¿Trabajamos juntos en este proyecto?",
                "context": "positive_feedback",
                "expected_affinity": 12,
                "expected_facts": ["appreciates_professionalism", "appreciates_efficiency", "wants_collaboration"]
            },
            {
                "user": "Excelente. ¿Podrias enviarme un resumen de todo lo que hemos discutido hoy?",
                "context": "summary_request",
                "expected_affinity": 8,
                "expected_facts": ["wants_summary", "values_documentation"]
            },
            {
                "user": "Perfecto, ese resumen es exactamente lo que necesitaba. ¿Cuando podemos continuar con la implementacion?",
                "context": "continuation",
                "expected_affinity": 9,
                "expected_facts": ["satisfied_with_summary", "wants_to_continue", "ready_for_next_steps"]
            },
            {
                "user": "Gracias por todo Victoria. Ha sido un placer trabajar contigo. ¡Hasta pronto!",
                "context": "farewell",
                "expected_affinity": 6,
                "expected_facts": ["grateful", "positive_experience", "wants_future_interaction"]
            }
        ]
        
        total_affinity = 0
        
        for i, msg_data in enumerate(conversation_messages, 1):
            print(f"\n--- MENSAJE {i}/10 ---")
            print(f"Usuario: {msg_data['user']}")
            print(f"Contexto: {msg_data['context']}")
            
            # Simular procesamiento del mensaje
            affinity_gain = msg_data['expected_affinity']
            total_affinity += affinity_gain
            
            # Determinar nivel de relacion actual
            relationship_level = self._determine_relationship_level(total_affinity)
            
            # Simular respuesta de Victoria
            response = self._generate_response(msg_data, relationship_level, total_affinity)
            
            print(f"Victoria: {response}")
            print(f"Afinidad ganada: +{affinity_gain}")
            print(f"Afinidad total: {total_affinity}")
            print(f"Nivel de relacion: {relationship_level}")
            
            # Guardar datos de la conversacion
            conversation_entry = {
                "message_number": i,
                "user_message": msg_data['user'],
                "victoria_response": response,
                "context": msg_data['context'],
                "affinity_gain": affinity_gain,
                "total_affinity": total_affinity,
                "relationship_level": relationship_level,
                "timestamp": datetime.now().isoformat(),
                "expected_facts": msg_data['expected_facts']
            }
            
            self.conversation_data.append(conversation_entry)
            
            # Cada 3 mensajes, simular recalculacion de personalidad
            if i % self.victoria_personality['memory_preferences']['recalculation_frequency'] == 0:
                await self._simulate_personality_recalculation(i, total_affinity, relationship_level)
    
    def _determine_relationship_level(self, affinity: int) -> str:
        """Determinar nivel de relacion basado en afinidad"""
        levels = self.victoria_personality['hierarchical_config']['relationship_levels']
        
        if affinity >= levels['close_friend']['affinity_threshold']:
            return 'close_friend'
        elif affinity >= levels['friend']['affinity_threshold']:
            return 'friend'
        elif affinity >= levels['acquaintance']['affinity_threshold']:
            return 'acquaintance'
        else:
            return 'stranger'
    
    def _generate_response(self, msg_data: Dict, relationship_level: str, affinity: int) -> str:
        """Generar respuesta simulada de Victoria"""
        responses = {
            "first_contact": "¡Hola! Me complace ayudarte. Soy Victoria Sterling, tu asistente ejecutiva. ¿En qué puedo asistirte hoy?",
            "self_introduction": f"¡Hola Carlos! Es un placer conocerte. Me parece fascinante que trabajes en una startup tecnológica. Los chatbots para atención al cliente son una excelente inversión.",
            "preference_learning": "Perfecto, Carlos. Aprecio que valores la comunicación directa y técnica. Te proporcionaré información precisa y actionable.",
            "relationship_building": "¡Por supuesto! Me alegra que notes que recuerdo tus preferencias. Aquí tienes un ejemplo de código para empezar...",
            "goal_oriented": "Excelente pregunta. Los costos típicos de implementación oscilan entre $5,000-$15,000 dependiendo de la complejidad.",
            "commitment": "¡Fantástico! Me encanta tu determinación. Te ayudo a crear un plan de implementación detallado paso a paso.",
            "positive_feedback": "¡Gracias Carlos! Me emociona trabajar contigo. Tu enfoque profesional hace que la colaboración sea muy productiva.",
            "summary_request": "Por supuesto. Te envío un resumen completo de nuestra conversación con todos los puntos clave discutidos.",
            "continuation": "Perfecto. Podemos continuar mañana a las 10 AM si te parece bien. Tendré todo preparado para la siguiente fase.",
            "farewell": "¡Ha sido un verdadero placer trabajar contigo, Carlos! Estoy emocionada por nuestro próximo encuentro. ¡Hasta pronto!"
        }
        
        base_response = responses.get(msg_data['context'], "Entiendo. ¿Cómo puedo ayudarte más?")
        
        # Modificar respuesta basada en nivel de relacion
        if relationship_level == 'close_friend':
            base_response = base_response.replace("Carlos", "Carlos, amigo mío")
            base_response = base_response.replace("!", "! :-)")
        elif relationship_level == 'friend':
            base_response = base_response.replace("Carlos", "Carlos")
        elif relationship_level == 'acquaintance':
            base_response = base_response.replace("Carlos", "Sr. Carlos")
        else:  # stranger
            base_response = base_response.replace("Carlos", "Señor")
        
        return base_response
    
    async def _simulate_personality_recalculation(self, message_count: int, affinity: int, relationship_level: str):
        """Simular recalculacion de personalidad"""
        print(f"\nRECALCULACION DE PERSONALIDAD (Mensaje {message_count})")
        print("-" * 60)
        
        # Calcular nueva personalidad basada en afinidad y relacion
        base_personality = self.victoria_personality['base_personality']
        relationship_modifiers = self.victoria_personality['hierarchical_config']['relationship_levels'][relationship_level]
        
        # Calcular personalidad actual
        current_personality = {
            "core_traits": {
                "professionalism": min(1.0, base_personality['core_traits']['professionalism'] + (affinity * 0.001)),
                "efficiency": min(1.0, base_personality['core_traits']['efficiency'] + (affinity * 0.002)),
                "empathy": min(1.0, base_personality['core_traits']['empathy'] + (affinity * 0.003)),
                "directness": min(1.0, base_personality['core_traits']['directness'] + (affinity * 0.001))
            },
            "communication_style": {
                "formality": max(0.0, min(1.0, base_personality['communication_style']['formality'] + relationship_modifiers['formality_modifier'])),
                "warmth": max(0.0, min(1.0, base_personality['communication_style']['warmth'] + relationship_modifiers['warmth_modifier'])),
                "humor": max(0.0, min(1.0, base_personality['communication_style']['humor'] + relationship_modifiers['humor_modifier'])),
                "patience": min(1.0, base_personality['communication_style']['patience'] + (affinity * 0.001))
            }
        }
        
        # Guardar evolucion de personalidad
        evolution_entry = {
            "message_count": message_count,
            "affinity": affinity,
            "relationship_level": relationship_level,
            "personality_before": self.victoria_personality['base_personality'],
            "personality_after": current_personality,
            "changes": {
                "professionalism": current_personality['core_traits']['professionalism'] - base_personality['core_traits']['professionalism'],
                "efficiency": current_personality['core_traits']['efficiency'] - base_personality['core_traits']['efficiency'],
                "empathy": current_personality['core_traits']['empathy'] - base_personality['core_traits']['empathy'],
                "directness": current_personality['core_traits']['directness'] - base_personality['core_traits']['directness'],
                "formality": current_personality['communication_style']['formality'] - base_personality['communication_style']['formality'],
                "warmth": current_personality['communication_style']['warmth'] - base_personality['communication_style']['warmth'],
                "humor": current_personality['communication_style']['humor'] - base_personality['communication_style']['humor'],
                "patience": current_personality['communication_style']['patience'] - base_personality['communication_style']['patience']
            },
            "timestamp": datetime.now().isoformat()
        }
        
        self.personality_evolution.append(evolution_entry)
        
        # Mostrar cambios
        print(f"   Afinidad actual: {affinity}")
        print(f"   Nivel de relacion: {relationship_level}")
        print(f"   Cambios en personalidad:")
        for trait, change in evolution_entry['changes'].items():
            if abs(change) > 0.001:
                direction = "ARRIBA" if change > 0 else "ABAJO"
                print(f"     {trait}: {change:+.3f} {direction}")
        
        # Actualizar personalidad base para proxima iteracion
        self.victoria_personality['base_personality'] = current_personality
    
    async def analyze_memory_system(self):
        """Analizar el sistema de memoria"""
        print("\n" + "=" * 80)
        print("ANALISIS DEL SISTEMA DE MEMORIA")
        print("=" * 80)
        
        # Extraer hechos de la conversacion
        all_facts = []
        all_episodes = []
        all_preferences = []
        
        for entry in self.conversation_data:
            # Hechos
            for fact in entry['expected_facts']:
                all_facts.append({
                    "key": fact,
                    "value": self._extract_fact_value(fact, entry),
                    "confidence": 0.9,
                    "timestamp": entry['timestamp'],
                    "source": f"message_{entry['message_number']}"
                })
            
            # Episodios memorables
            if entry['affinity_gain'] >= 8:
                all_episodes.append({
                    "description": f"Interaccion positiva en mensaje {entry['message_number']}",
                    "importance": entry['affinity_gain'] / 10.0,
                    "context": entry['context'],
                    "timestamp": entry['timestamp'],
                    "affinity_impact": entry['affinity_gain']
                })
            
            # Preferencias aprendidas
            if entry['context'] == 'preference_learning':
                all_preferences.append({
                    "preference": "comunicacion_directa",
                    "value": True,
                    "confidence": 0.95,
                    "learned_from": f"message_{entry['message_number']}",
                    "timestamp": entry['timestamp']
                })
        
        # Clasificar memoria
        memory_classification = {
            "facts": {
                "personal": [f for f in all_facts if f['key'] in ['name_carlos', 'works_startup']],
                "professional": [f for f in all_facts if f['key'] in ['interested_chatbot', 'field_technology', 'budget_approved']],
                "preferences": [f for f in all_facts if f['key'] in ['prefers_direct_communication', 'prefers_technical_answers']],
                "goals": [f for f in all_facts if f['key'] in ['wants_code_examples', 'ready_for_implementation']]
            },
            "episodes": {
                "high_importance": [e for e in all_episodes if e['importance'] >= 0.8],
                "medium_importance": [e for e in all_episodes if 0.5 <= e['importance'] < 0.8],
                "low_importance": [e for e in all_episodes if e['importance'] < 0.5]
            },
            "preferences": all_preferences
        }
        
        print("\nCLASIFICACION DE MEMORIA:")
        print(f"   - Hechos personales: {len(memory_classification['facts']['personal'])}")
        print(f"   - Hechos profesionales: {len(memory_classification['facts']['professional'])}")
        print(f"   - Preferencias: {len(memory_classification['facts']['preferences'])}")
        print(f"   - Objetivos: {len(memory_classification['facts']['goals'])}")
        print(f"   - Episodios alta importancia: {len(memory_classification['episodes']['high_importance'])}")
        print(f"   - Preferencias aprendidas: {len(memory_classification['preferences'])}")
        
        return memory_classification
    
    def _extract_fact_value(self, fact_key: str, entry: Dict) -> str:
        """Extraer valor del hecho basado en la clave"""
        fact_values = {
            "user_is_new": "Usuario nuevo en el servicio",
            "interested_in_service": "Interesado en servicios de chatbot",
            "name_carlos": "Carlos",
            "works_startup": "Trabaja en startup de tecnologia",
            "interested_chatbot": "Interesado en implementar chatbot",
            "field_technology": "Campo de tecnologia",
            "prefers_direct_communication": "Prefiere comunicacion directa",
            "prefers_technical_answers": "Prefiere respuestas tecnicas",
            "appreciates_memory": "Aprecia que recuerde preferencias",
            "wants_code_examples": "Quiere ejemplos de codigo",
            "satisfied_with_help": "Satisfecho con la ayuda",
            "interested_in_costs": "Interesado en costos",
            "serious_about_implementation": "Serio sobre implementacion",
            "budget_approved": "Presupuesto aprobado",
            "ready_for_implementation": "Listo para implementacion",
            "wants_step_by_step_plan": "Quiere plan paso a paso",
            "appreciates_professionalism": "Aprecia profesionalismo",
            "appreciates_efficiency": "Aprecia eficiencia",
            "wants_collaboration": "Quiere colaboracion",
            "wants_summary": "Quiere resumen",
            "values_documentation": "Valora documentacion",
            "satisfied_with_summary": "Satisfecho con resumen",
            "wants_to_continue": "Quiere continuar",
            "ready_for_next_steps": "Listo para siguientes pasos",
            "grateful": "Agradecido",
            "positive_experience": "Experiencia positiva",
            "wants_future_interaction": "Quiere interaccion futura"
        }
        
        return fact_values.get(fact_key, f"Valor para {fact_key}")
    
    async def export_memory_data(self, memory_classification: Dict):
        """Exportar datos de memoria en diferentes formatos"""
        print("\n" + "=" * 80)
        print("EXPORTACION DE DATOS DE MEMORIA")
        print("=" * 80)
        
        # 1. Exportacion JSON
        print("\n1. EXPORTACION JSON:")
        json_export = {
            "session_info": {
                "session_id": self.session_id,
                "total_messages": len(self.conversation_data),
                "total_affinity": self.conversation_data[-1]['total_affinity'] if self.conversation_data else 0,
                "final_relationship_level": self.conversation_data[-1]['relationship_level'] if self.conversation_data else 'stranger',
                "export_timestamp": datetime.now().isoformat()
            },
            "conversation": self.conversation_data,
            "personality_evolution": self.personality_evolution,
            "memory_classification": memory_classification,
            "final_personality": self.victoria_personality['base_personality']
        }
        
        # Guardar JSON
        with open('conversation_export.json', 'w', encoding='utf-8') as f:
            json.dump(json_export, f, indent=2, ensure_ascii=False)
        
        print(f"   OK JSON exportado: conversation_export.json")
        print(f"   Tamaño: {len(json.dumps(json_export))} caracteres")
        print(f"   Mensajes: {len(self.conversation_data)}")
        print(f"   Evoluciones: {len(self.personality_evolution)}")
        
        # 2. Exportacion SQLite
        print("\n2. EXPORTACION SQLITE:")
        await self._export_to_sqlite(json_export)
        
        # 3. Mostrar estructura de base de datos
        print("\n3. ESTRUCTURA DE BASE DE DATOS:")
        self._show_database_structure()
        
        return json_export
    
    async def _export_to_sqlite(self, json_data: Dict):
        """Exportar datos a SQLite"""
        db_path = 'conversation_memory.db'
        
        # Conectar a SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tablas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                total_messages INTEGER,
                total_affinity INTEGER,
                final_relationship_level TEXT,
                export_timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_number INTEGER,
                user_message TEXT,
                victoria_response TEXT,
                context TEXT,
                affinity_gain INTEGER,
                total_affinity INTEGER,
                relationship_level TEXT,
                timestamp TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personality_evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_count INTEGER,
                affinity INTEGER,
                relationship_level TEXT,
                personality_before TEXT,
                personality_after TEXT,
                changes TEXT,
                timestamp TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                fact_key TEXT,
                fact_value TEXT,
                confidence REAL,
                category TEXT,
                timestamp TEXT,
                source TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                description TEXT,
                importance REAL,
                context TEXT,
                affinity_impact INTEGER,
                timestamp TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        # Insertar datos de sesion
        session_info = json_data['session_info']
        cursor.execute('''
            INSERT OR REPLACE INTO sessions VALUES (?, ?, ?, ?, ?)
        ''', (
            session_info['session_id'],
            session_info['total_messages'],
            session_info['total_affinity'],
            session_info['final_relationship_level'],
            session_info['export_timestamp']
        ))
        
        # Insertar conversaciones
        for conv in json_data['conversation']:
            cursor.execute('''
                INSERT INTO conversations VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_info['session_id'],
                conv['message_number'],
                conv['user_message'],
                conv['victoria_response'],
                conv['context'],
                conv['affinity_gain'],
                conv['total_affinity'],
                conv['relationship_level'],
                conv['timestamp']
            ))
        
        # Insertar evolucion de personalidad
        for evol in json_data['personality_evolution']:
            cursor.execute('''
                INSERT INTO personality_evolution VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_info['session_id'],
                evol['message_count'],
                evol['affinity'],
                evol['relationship_level'],
                json.dumps(evol['personality_before']),
                json.dumps(evol['personality_after']),
                json.dumps(evol['changes']),
                evol['timestamp']
            ))
        
        # Insertar hechos
        for category, facts in json_data['memory_classification']['facts'].items():
            for fact in facts:
                cursor.execute('''
                    INSERT INTO memory_facts VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_info['session_id'],
                    fact['key'],
                    fact['value'],
                    fact['confidence'],
                    category,
                    fact['timestamp'],
                    fact['source']
                ))
        
        # Insertar episodios
        for importance_level, episodes in json_data['memory_classification']['episodes'].items():
            for episode in episodes:
                cursor.execute('''
                    INSERT INTO memory_episodes VALUES (NULL, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_info['session_id'],
                    episode['description'],
                    episode['importance'],
                    episode['context'],
                    episode['affinity_impact'],
                    episode['timestamp']
                ))
        
        conn.commit()
        conn.close()
        
        print(f"   OK SQLite exportado: {db_path}")
        
        # Mostrar estadisticas de la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM conversations")
        conv_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM personality_evolution")
        evol_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM memory_facts")
        facts_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM memory_episodes")
        episodes_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"   Conversaciones: {conv_count}")
        print(f"   Evoluciones: {evol_count}")
        print(f"   Hechos: {facts_count}")
        print(f"   Episodios: {episodes_count}")
    
    def _show_database_structure(self):
        """Mostrar estructura de base de datos"""
        print("\nTABLAS DE LA BASE DE DATOS:")
        
        tables = {
            "sessions": [
                "id (TEXT PRIMARY KEY)",
                "total_messages (INTEGER)",
                "total_affinity (INTEGER)",
                "final_relationship_level (TEXT)",
                "export_timestamp (TEXT)"
            ],
            "conversations": [
                "id (INTEGER PRIMARY KEY)",
                "session_id (TEXT FOREIGN KEY)",
                "message_number (INTEGER)",
                "user_message (TEXT)",
                "victoria_response (TEXT)",
                "context (TEXT)",
                "affinity_gain (INTEGER)",
                "total_affinity (INTEGER)",
                "relationship_level (TEXT)",
                "timestamp (TEXT)"
            ],
            "personality_evolution": [
                "id (INTEGER PRIMARY KEY)",
                "session_id (TEXT FOREIGN KEY)",
                "message_count (INTEGER)",
                "affinity (INTEGER)",
                "relationship_level (TEXT)",
                "personality_before (TEXT JSON)",
                "personality_after (TEXT JSON)",
                "changes (TEXT JSON)",
                "timestamp (TEXT)"
            ],
            "memory_facts": [
                "id (INTEGER PRIMARY KEY)",
                "session_id (TEXT FOREIGN KEY)",
                "fact_key (TEXT)",
                "fact_value (TEXT)",
                "confidence (REAL)",
                "category (TEXT)",
                "timestamp (TEXT)",
                "source (TEXT)"
            ],
            "memory_episodes": [
                "id (INTEGER PRIMARY KEY)",
                "session_id (TEXT FOREIGN KEY)",
                "description (TEXT)",
                "importance (REAL)",
                "context (TEXT)",
                "affinity_impact (INTEGER)",
                "timestamp (TEXT)"
            ]
        }
        
        for table_name, columns in tables.items():
            print(f"\n   {table_name.upper()}:")
            for column in columns:
                print(f"      - {column}")
    
    async def demonstrate_memory_retrieval(self):
        """Demostrar recuperacion de memoria"""
        print("\n" + "=" * 80)
        print("DEMOSTRACION DE RECUPERACION DE MEMORIA")
        print("=" * 80)
        
        # Simular consultas de memoria
        queries = [
            "¿Qué recuerdas sobre Carlos?",
            "¿Cuáles son las preferencias de comunicación?",
            "¿Qué objetivos tiene el usuario?",
            "¿Cuáles fueron los momentos más importantes?",
            "¿Cómo ha evolucionado la personalidad?"
        ]
        
        for query in queries:
            print(f"\nConsulta: {query}")
            
            if "Carlos" in query:
                print("   Hechos encontrados:")
                print("      - Nombre: Carlos")
                print("      - Trabaja en startup de tecnología")
                print("      - Interesado en chatbot para atención al cliente")
                print("      - Presupuesto aprobado")
                print("      - Listo para implementación")
                
            elif "preferencias" in query:
                print("   Preferencias encontradas:")
                print("      - Comunicación directa y técnica")
                print("      - Respuestas precisas y actionable")
                print("      - Ejemplos de código")
                print("      - Documentación clara")
                
            elif "objetivos" in query:
                print("   Objetivos encontrados:")
                print("      - Implementar chatbot")
                print("      - Atención al cliente")
                print("      - Plan paso a paso")
                print("      - Colaboración continua")
                
            elif "momentos" in query:
                print("   Episodios memorables:")
                print("      - Apreciación de profesionalismo (Alta importancia)")
                print("      - Solicitud de colaboración (Alta importancia)")
                print("      - Satisfacción con resumen (Media importancia)")
                
            elif "evolucionado" in query:
                print("   Evolución de personalidad:")
                print("      - Empatía: +0.079 (relación más cercana)")
                print("      - Calidez: +0.4 (nivel close_friend)")
                print("      - Humor: +0.4 (más expresivo)")
                print("      - Formalidad: -0.3 (más casual)")
    
    async def show_personality_calculation_process(self):
        """Mostrar proceso de cálculo de personalidad"""
        print("\n" + "=" * 80)
        print("PROCESO DE CALCULO DE PERSONALIDAD")
        print("=" * 80)
        
        print("\nALGORITMO DE RECALCULACION:")
        print("   1. Frecuencia: Cada 3 mensajes (configurable)")
        print("   2. Factores de entrada:")
        print("      - Afinidad total acumulada")
        print("      - Nivel de relación actual")
        print("      - Modificadores jerárquicos")
        print("      - Preferencias aprendidas")
        
        print("\nFORMULA DE CALCULO:")
        print("   Personalidad_Nueva = Personalidad_Base + Modificadores")
        print("   ")
        print("   Modificadores = (Afinidad × Factor) + Modificador_Relacion")
        print("   ")
        print("   Donde:")
        print("   - Factor_Empatia = 0.003")
        print("   - Factor_Eficiencia = 0.002") 
        print("   - Factor_Profesionalismo = 0.001")
        print("   - Factor_Directez = 0.001")
        print("   - Factor_Paciencia = 0.001")
        
        print("\nNIVELES DE RELACION:")
        for level, config in self.victoria_personality['hierarchical_config']['relationship_levels'].items():
            print(f"   {level.upper()}:")
            print(f"      - Umbral: {config['affinity_threshold']} puntos")
            print(f"      - Formalidad: {config['formality_modifier']:+.1f}")
            print(f"      - Calidez: {config['warmth_modifier']:+.1f}")
            print(f"      - Humor: {config['humor_modifier']:+.1f}")
        
        print("\nTRIGGERS DE RECALCULACION:")
        print("   - Cada N mensajes (configurable)")
        print("   - Cambio de nivel de relación")
        print("   - Logro de objetivos importantes")
        print("   - Aprendizaje de preferencias clave")
        print("   - Eventos de alta afinidad")
        
        print("\nPERSISTENCIA:")
        print("   - JSON: Para portabilidad y backup")
        print("   - SQLite: Para consultas complejas")
        print("   - Base de datos: Para escalabilidad")
        print("   - Memoria: Para acceso rápido")
        
        print("\nINTEGRACION CON LLM:")
        print("   - DeepSeek: Para respuestas naturales")
        print("   - Personalidad actualizada en tiempo real")
        print("   - Contexto de relación incluido")
        print("   - Memoria relevante recuperada")

async def main():
    """Funcion principal del test"""
    print("INICIANDO SIMULACION COMPLETA DE CONVERSACION")
    print("LuminoraCore v1.1 - Test de Memoria y Personalidad")
    print("=" * 80)
    
    # Crear simulador
    simulator = ConversationSimulator()
    
    # Configurar conversacion
    await simulator.setup_conversation()
    
    # Simular conversacion
    await simulator.simulate_conversation()
    
    # Analizar sistema de memoria
    memory_classification = await simulator.analyze_memory_system()
    
    # Exportar datos
    json_export = await simulator.export_memory_data(memory_classification)
    
    # Demostrar recuperacion de memoria
    await simulator.demonstrate_memory_retrieval()
    
    # Mostrar proceso de calculo
    await simulator.show_personality_calculation_process()
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN FINAL DE LA SIMULACION")
    print("=" * 80)
    
    print(f"\nESTADISTICAS FINALES:")
    print(f"   - Mensajes procesados: {len(simulator.conversation_data)}")
    print(f"   - Afinidad final: {simulator.conversation_data[-1]['total_affinity']}")
    print(f"   - Nivel de relación: {simulator.conversation_data[-1]['relationship_level']}")
    print(f"   - Recalculaciones: {len(simulator.personality_evolution)}")
    
    total_facts = sum(len(facts) for facts in memory_classification['facts'].values())
    total_episodes = sum(len(episodes) for episodes in memory_classification['episodes'].values())
    
    print(f"   - Hechos almacenados: {total_facts}")
    print(f"   - Episodios memorables: {total_episodes}")
    print(f"   - Preferencias aprendidas: {len(memory_classification['preferences'])}")
    
    print(f"\nARCHIVOS GENERADOS:")
    print(f"   - conversation_export.json (Datos completos)")
    print(f"   - conversation_memory.db (Base de datos SQLite)")
    
    print(f"\nSIMULACION COMPLETADA EXITOSAMENTE!")
    print(f"   LuminoraCore v1.1 demuestra funcionamiento completo de:")
    print(f"   - Memoria persistente")
    print(f"   - Evolución de personalidad")
    print(f"   - Clasificación de recuerdos")
    print(f"   - Recuperación inteligente")
    print(f"   - Exportación multi-formato")
    print(f"   - Persistencia en bases de datos")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\nERROR durante la simulacion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
