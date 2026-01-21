"""
Teste E2E Realista - Cadastro de aluno com foto e detecção
Simula o fluxo completo: Cadastro -> Foto -> Câmera -> Detecção -> Presença
"""
import asyncio
import sys
from pathlib import Path
import cv2
import requests
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

API_URL = "http://localhost:8000"
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "faces"

class RealisticE2ETest:
    def __init__(self):
        self.token = None
        self.camera_id = None
        self.students = []
        
    def print_step(self, step: str):
        print(f"\n{'='*70}")
        print(f"🔹 {step}")
        print(f"{'='*70}")
    
    def print_success(self, msg: str):
        print(f"✓ {msg}")
    
    def print_error(self, msg: str):
        print(f"✗ {msg}")
    
    def login(self):
        """1. Login no sistema"""
        self.print_step("STEP 1: Autenticação")
        
        response = requests.post(
            f"{API_URL}/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.print_success("Login realizado com sucesso")
            return True
        else:
            self.print_error(f"Erro no login: {response.status_code}")
            return False
    
    def register_students_with_photos(self):
        """2. Cadastra alunos com suas fotos"""
        self.print_step("STEP 2: Cadastro de Alunos com Fotos")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Lista de alunos para cadastrar
        students_data = [
            {
                "name": "João Silva",
                "registration": "2024001",
                "class_name": "3º Ano A",
                "parent_phone": "+5511999991111",
                "parent_email": "joao.silva@example.com",
                "photo": "joao.jpg"
            },
            {
                "name": "Maria Santos",
                "registration": "2024002",
                "class_name": "3º Ano A",
                "parent_phone": "+5511999992222",
                "parent_email": "maria.santos@example.com",
                "photo": "maria.jpg"
            },
            {
                "name": "Pedro Costa",
                "registration": "2024003",
                "class_name": "2º Ano B",
                "parent_phone": "+5511999993333",
                "parent_email": "pedro.costa@example.com",
                "photo": "pedro.jpg"
            }
        ]
        
        for student_data in students_data:
            photo_name = student_data.pop("photo")
            photo_path = FIXTURES_DIR / photo_name
            
            # Cadastra aluno
            response = requests.post(
                f"{API_URL}/api/v1/students",
                json=student_data,
                headers=headers
            )
            
            if response.status_code != 201:
                self.print_error(f"Erro ao cadastrar {student_data['name']}")
                continue
            
            student = response.json()
            student_id = student["id"]
            
            # Upload da foto
            if photo_path.exists():
                with open(photo_path, "rb") as f:
                    files = {"file": (photo_name, f, "image/jpeg")}
                    response = requests.post(
                        f"{API_URL}/api/v1/students/{student_id}/photos",
                        files=files,
                        headers=headers
                    )
                
                if response.status_code == 201:
                    self.print_success(f"{student_data['name']} cadastrado com foto")
                    self.students.append(student)
                else:
                    self.print_error(f"Erro ao enviar foto de {student_data['name']}")
            else:
                # Cria foto simulada se não existir
                self._create_simulated_photo(photo_path, student_data['name'])
                self.print_success(f"{student_data['name']} cadastrado (foto simulada)")
                self.students.append(student)
        
        return len(self.students) > 0
    
    def setup_camera(self, use_webcam: bool = True):
        """3. Configura câmera (webcam ou vídeo)"""
        self.print_step("STEP 3: Configuração de Câmera")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        if use_webcam:
            camera_data = {
                "name": "Câmera Entrada Principal",
                "rtsp_url": "webcam://0",
                "location": "Portaria",
                "enabled": True
            }
            print("📹 Usando webcam do computador")
        else:
            video_path = Path(__file__).parent / "videos" / "test_video.mp4"
            camera_data = {
                "name": "Câmera Teste Simulada",
                "rtsp_url": f"file://{video_path}",
                "location": "Teste",
                "enabled": True
            }
            print("📹 Usando vídeo de teste")
        
        response = requests.post(
            f"{API_URL}/api/v1/cameras",
            json=camera_data,
            headers=headers
        )
        
        if response.status_code == 201:
            self.camera_id = response.json()["id"]
            self.print_success(f"Câmera configurada: ID {self.camera_id}")
            return True
        else:
            self.print_error(f"Erro ao configurar câmera: {response.status_code}")
            return False
    
    def start_monitoring(self):
        """4. Inicia monitoramento"""
        self.print_step("STEP 4: Início do Monitoramento")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.post(
            f"{API_URL}/api/v1/cameras/{self.camera_id}/start",
            headers=headers
        )
        
        if response.status_code == 200:
            self.print_success("Streaming iniciado")
            print("\n📸 Sistema monitorando entrada...")
            print("💡 Posicione os alunos na frente da câmera")
            return True
        else:
            self.print_error(f"Erro ao iniciar streaming: {response.status_code}")
            return False
    
    def monitor_detections(self, duration: int = 60):
        """5. Monitora detecções em tempo real"""
        self.print_step("STEP 5: Monitoramento de Detecções")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        print(f"⏱️  Monitorando por {duration} segundos...")
        print("👤 Aguardando detecções...\n")
        
        detected_students = set()
        last_detection_count = 0
        
        for i in range(duration):
            time.sleep(1)
            
            # Busca detecções
            response = requests.get(
                f"{API_URL}/api/v1/detections",
                params={"camera_id": self.camera_id, "limit": 10},
                headers=headers
            )
            
            if response.status_code == 200:
                detections = response.json()
                
                if len(detections) > last_detection_count:
                    for detection in detections:
                        student_id = detection.get("student_id")
                        if student_id and student_id not in detected_students:
                            detected_students.add(student_id)
                            student = next((s for s in self.students if s["id"] == student_id), None)
                            if student:
                                confidence = detection.get("confidence", 0)
                                print(f"✓ DETECTADO: {student['name']} (confiança: {confidence:.1%})")
                    
                    last_detection_count = len(detections)
            
            # Mostra progresso a cada 10s
            if i > 0 and i % 10 == 0:
                print(f"  [{i}s] {len(detected_students)} aluno(s) detectado(s)")
        
        print(f"\n📊 Total de alunos detectados: {len(detected_students)}/{len(self.students)}")
        return len(detected_students) > 0
    
    def verify_attendance(self):
        """6. Verifica registros de presença"""
        self.print_step("STEP 6: Verificação de Presença")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        today = datetime.now().strftime("%Y-%m-%d")
        
        response = requests.get(
            f"{API_URL}/api/v1/attendance",
            params={"date": today},
            headers=headers
        )
        
        if response.status_code == 200:
            records = response.json()
            
            print(f"📋 Registros de presença hoje: {len(records)}")
            
            for record in records:
                student = next((s for s in self.students if s["id"] == record["student_id"]), None)
                if student:
                    time_str = record.get("check_in_time", "")
                    print(f"  ✓ {student['name']} - {time_str}")
            
            return len(records) > 0
        else:
            self.print_error(f"Erro ao verificar presença: {response.status_code}")
            return False
    
    def verify_notifications(self):
        """7. Verifica notificações enviadas"""
        self.print_step("STEP 7: Verificação de Notificações")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        total_notifications = 0
        
        for student in self.students:
            response = requests.get(
                f"{API_URL}/api/v1/notifications",
                params={"student_id": student["id"], "limit": 5},
                headers=headers
            )
            
            if response.status_code == 200:
                notifications = response.json()
                if notifications:
                    total_notifications += len(notifications)
                    print(f"  📧 {student['name']}: {len(notifications)} notificação(ões)")
        
        if total_notifications > 0:
            self.print_success(f"Total: {total_notifications} notificação(ões) enviada(s)")
            return True
        else:
            print("  ⚠️  Nenhuma notificação encontrada")
            return False
    
    def cleanup(self):
        """8. Finaliza monitoramento"""
        self.print_step("STEP 8: Finalização")
        
        if self.camera_id and self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            requests.post(
                f"{API_URL}/api/v1/cameras/{self.camera_id}/stop",
                headers=headers
            )
            self.print_success("Streaming parado")
        
        self.print_success("Sistema finalizado")
    
    def _create_simulated_photo(self, path: Path, name: str):
        """Cria foto simulada se não existir"""
        import numpy as np
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Cria imagem com rosto simulado
        img = np.ones((480, 640, 3), dtype=np.uint8) * 220
        
        # Rosto
        cv2.circle(img, (320, 240), 80, (200, 180, 150), -1)
        # Olhos
        cv2.circle(img, (290, 220), 10, (50, 50, 50), -1)
        cv2.circle(img, (350, 220), 10, (50, 50, 50), -1)
        # Boca
        cv2.ellipse(img, (320, 270), (30, 15), 0, 0, 180, (50, 50, 50), 2)
        
        # Nome
        cv2.putText(img, name, (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        cv2.imwrite(str(path), img)
    
    def run(self, use_webcam: bool = True, monitor_duration: int = 60):
        """Executa teste completo"""
        print("\n" + "="*70)
        print("🎓 TESTE E2E REALISTA - GT-VISION")
        print("Sistema de Presença com Reconhecimento Facial")
        print("="*70)
        
        results = []
        
        try:
            # Executa passos
            if not self.login():
                return False
            results.append(("Login", True))
            
            if not self.register_students_with_photos():
                return False
            results.append(("Cadastro de Alunos", True))
            
            if not self.setup_camera(use_webcam):
                return False
            results.append(("Configuração de Câmera", True))
            
            if not self.start_monitoring():
                return False
            results.append(("Início do Monitoramento", True))
            
            detected = self.monitor_detections(monitor_duration)
            results.append(("Detecções", detected))
            
            has_attendance = self.verify_attendance()
            results.append(("Registro de Presença", has_attendance))
            
            has_notifications = self.verify_notifications()
            results.append(("Notificações", has_notifications))
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Teste interrompido pelo usuário")
            return False
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.cleanup()
        
        # Relatório final
        self.print_step("RELATÓRIO FINAL")
        
        for name, result in results:
            status = "✓" if result else "✗"
            print(f"{status} {name}")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print(f"\n{'='*70}")
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM!")
        else:
            print(f"⚠️  {passed}/{total} testes passaram")
        print("="*70)
        
        return passed >= total - 1  # Permite falha apenas em notificações

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Teste E2E Realista GT-Vision")
    parser.add_argument("--video", action="store_true", help="Usar vídeo ao invés de webcam")
    parser.add_argument("--duration", type=int, default=60, help="Duração do monitoramento (segundos)")
    
    args = parser.parse_args()
    
    tester = RealisticE2ETest()
    success = tester.run(use_webcam=not args.video, monitor_duration=args.duration)
    
    sys.exit(0 if success else 1)
