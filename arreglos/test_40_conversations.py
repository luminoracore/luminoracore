#!/usr/bin/env python3
"""
Script de prueba con 40 conversaciones - Versión mejorada con guardado de progreso
"""

import requests
import json
import time
from datetime import datetime

class LuminoraMemoryTester:
    def __init__(self):
        self.base_url = "https://nxdsjksrga.execute-api.eu-west-1.amazonaws.com"
        self.session_id = f"test_session_{int(time.time())}"
        self.user_id = f"test_user_{int(time.time())}"
        self.token = None
        self.conversations = []
        self.facts_evolution = []
        self.sentiment_history = []
        
    def get_jwt_token(self):
        """Obtener token JWT"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/token",
                json={"user_id": self.user_id, "username": "testuser"},
                timeout=10
            )
            if response.status_code == 200:
                self.token = response.json().get('token')
                return True
        except:
            pass
        return False
    
    def send_message(self, message, personality="friendly_assistant"):
        """Enviar mensaje y obtener respuesta"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "session_id": self.session_id,
            "message": message,
            "personality_name": personality
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/chat",
                json=data,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def analyze_sentiment(self):
        """Analizar sentimiento de la sesión"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/sentiment/analyze/{self.session_id}",
                json={"text": "test"},
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def get_conversation_facts(self):
        """Obtener facts de la conversación"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/memory/session/{self.session_id}/facts",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('facts', [])
        except:
            pass
        return []
    
    def export_session(self):
        """Exportar sesión completa"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/session/{self.session_id}/export",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def run_phase(self, conversation_set, emotion, phase_num):
        """Ejecutar una fase de conversaciones"""
        print(f"\n{'='*80}")
        print(f"FASE {phase_num}: {emotion.upper()}")
        print('='*80)
        
        results = []
        
        for i, (user_msg, description) in enumerate(conversation_set, 1):
            print(f"[{i}/{len(conversation_set)}] {description}")
            
            response = self.send_message(user_msg)
            
            if response:
                assistant_msg = response.get('response', '')
                facts_count = response.get('memory_facts_count', 0)
                new_facts_count = response.get('new_facts_count', 0)
                new_facts = response.get('new_facts', [])
                
                print(f"  Facts: {facts_count} totales, {new_facts_count} nuevos")
                
                results.append({
                    "turn": len(self.conversations) + i,
                    "user_message": user_msg,
                    "assistant_response": assistant_msg,
                    "emotion": emotion,
                    "facts_count": facts_count,
                    "new_facts": new_facts
                })
                
                time.sleep(0.5)  # Pequeña pausa
        
        self.conversations.extend(results)
        
        # Guardar snapshot de facts
        facts = self.get_conversation_facts()
        self.facts_evolution.append({
            "phase": phase_num,
            "emotion": emotion,
            "conversation_count": len(self.conversations),
            "facts": facts,
            "facts_count": len(facts),
            "timestamp": datetime.now().isoformat()
        })
        
        # Analizar sentiment
        sentiment = self.analyze_sentiment()
        if sentiment:
            self.sentiment_history.append({
                "phase": phase_num,
                "emotion": emotion,
                "sentiment": sentiment,
                "timestamp": datetime.now().isoformat()
            })
        
        return results
    
    def run_test(self):
        """Ejecutar prueba completa"""
        print("\n🚀 PRUEBA DE 40 CONVERSACIONES - MEMORIA Y EVOLUCIÓN")
        print(f"🆔 Session: {self.session_id}\n")
        
        if not self.get_jwt_token():
            print("❌ Error obteniendo token")
            return
        
        # Fase 1: Contexto inicial (alegría)
        phase1 = [
            ("Hola, soy Alex, tengo 28 años", "Nombre y edad"),
            ("Trabajo como desarrollador en Madrid", "Profesión"),
            ("Me encanta la programación Python", "Interés profesional"),
            ("En mi tiempo libre leo ciencia ficción", "Hobby - Lectura"),
            ("Juego al fútbol los fines de semana", "Actividad"),
            ("Tengo dos hermanos", "Familia"),
            ("Estoy aprendiendo guitarra", "Nuevo hobby"),
            ("Mi comida favorita es la paella", "Gustos"),
            ("Soy fan de Star Wars", "Intereses"),
            ("Quisiera visitar Japón", "Aspiración")
        ]
        
        self.run_phase(phase1, "positive", 1)
        
        # Fase 2: Emociones positivas intensas (alegría extrema)
        phase2 = [
            ("¡Hoy me dieron un aumento de sueldo!", "Éxito laboral"),
            ("¡Es increíble! Todo está perfecto", "Optimismo"),
            ("Me siento genial y feliz", "Estado emocional"),
            ("¡Encontré el trabajo de mis sueños!", "Logro"),
            ("Mi familia está muy orgullosa", "Felicidad familiar"),
            ("Todo va de maravilla", "Optimismo general"),
            ("Me encanta cómo salen las cosas", "Satisfacción"),
            ("Es la mejor noticia en meses", "Emoción"),
            ("Estoy en la cima del mundo", "Estado máximo"),
            ("Quiero compartir mi felicidad contigo", "Deseo compartir")
        ]
        
        self.run_phase(phase2, "joy", 2)
        
        # Fase 3: Emociones negativas (enfado)
        phase3 = [
            ("Estoy muy molesto con lo que pasó", "Frustración"),
            ("No puedo creerlo, estoy furioso", "Enojo"),
            ("Esto es injusto y me enoja", "Injusticia"),
            ("Estoy disgustado con la situación", "Disgusto"),
            ("No entiendo por qué es tan complicado", "Frustración"),
            ("Esto me está sacando de quicio", "Irritación"),
            ("Me siento muy frustrado", "Frustración emocional"),
            ("Es molesto que no salga como quiero", "Molestia"),
            ("Estoy harto de que salga mal", "Cansancio"),
            ("Ya no puedo más con esto", "Agotamiento")
        ]
        
        self.run_phase(phase3, "anger", 3)
        
        # Fase 4: Resolución (balance emocional)
        phase4 = [
            ("Gracias por escucharme, me siento mejor", "Mejora"),
            ("Me alegra conversar contigo", "Gratitud"),
            ("Ahora puedo manejar mejor las situaciones", "Autoeficacia"),
            ("He aprendido mucho", "Aprendizaje"),
            ("Quiero seguir conversando", "Continuidad"),
            ("Eres muy buen conversador", "Compliment"),
            ("Espero que recordemos esto", "Memoria"),
            ("Ha sido un placer", "Cortesía"),
            ("Hasta pronto", "Despedida"),
            ("Gracias por todo", "Agradecimiento")
        ]
        
        self.run_phase(phase4, "resolved", 4)
        
        # Exportar todo
        print("\n" + "="*80)
        print("EXPORTANDO DATOS...")
        print("="*80)
        
        session_export = self.export_session()
        
        # Crear reporte
        report = {
            "test_metadata": {
                "session_id": self.session_id,
                "user_id": self.user_id,
                "total_conversations": len(self.conversations),
                "timestamp": datetime.now().isoformat()
            },
            "conversations": self.conversations,
            "facts_evolution": self.facts_evolution,
            "sentiment_history": self.sentiment_history,
            "session_export": session_export
        }
        
        # Guardar
        filename = f"test_40_conversations_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Reporte guardado: {filename}")
        
        # Resumen
        print("\n" + "="*80)
        print("📊 RESUMEN FINAL")
        print("="*80)
        print(f"Total conversaciones: {len(self.conversations)}")
        print(f"Facts finales: {len(self.facts_evolution[-1]['facts']) if self.facts_evolution else 0}")
        print(f"Fases sentiment: {len(self.sentiment_history)}")
        
        print("\n📈 EVOLUCIÓN DE FACTS:")
        for phase in self.facts_evolution:
            print(f"   Fase {phase['phase']} ({phase['emotion']}): {phase['facts_count']} facts")
        
        print("\n😊 SENTIMENT POR FASE:")
        for sent in self.sentiment_history:
            print(f"   Fase {sent['phase']} ({sent['emotion']}): {sent.get('sentiment', {}).get('sentiment', 'N/A')}")
        
        print(f"\n💾 Datos completos exportados en: {filename}")


if __name__ == "__main__":
    tester = LuminoraMemoryTester()
    tester.run_test()
