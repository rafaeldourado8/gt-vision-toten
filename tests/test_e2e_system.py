"""
Teste E2E completo do sistema GT-Vision
Testa: Streaming -> Detecção -> Registro de Presença -> Notificação
"""
import asyncio
import sys
from pathlib import Path
import cv2
import requests
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

API_URL = "http://localhost:8000"
MEDIAMTX_URL = "http://localhost:8888"

class SystemTester:
    def __init__(self):
        self.token = None
        self.camera_id = None
        self.student_id = None
        
    def print_step(self, step: str):
        print(f"\n{'='*60}")
        print(f"🔹 {step}")
        print(f"{'='*60}")
    
    def login(self):
        """1. Login no sistema"""
        self.print_step("STEP 1: Login")
        
        response = requests.post(
            f"{API_URL}/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            print("✓ Login realizado com sucesso")
            return True
        else:
            print(f"✗ Erro no login: {response.status_code}")
            return False
    
    def create_student(self):
        """2. Cadastra aluno de teste"""
        self.print_step("STEP 2: Cadastrar Aluno")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        student_data = {
            "name": "João da Silva Teste",
            "registration": "TEST001",
            "class_name": "3º Ano A",
            "parent_phone": "+5511999999999",
            "parent_email": "teste@example.com"
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/students",
            json=student_data,
            headers=headers
        )
        
        if response.status_code == 201:
            self.student_id = response.json()["id"]
            print(f"✓ Aluno criado: ID {self.student_id}")
            return True
        else:
            print(f"✗ Erro ao criar aluno: {response.status_code}")
            return False
    
    def upload_student_photo(self):
        """3. Upload foto do aluno"""
        self.print_step("STEP 3: Upload Foto do Aluno")
        
        # Cria uma foto de teste
        img = cv2.imread(str(Path(__file__).parent / "fixtures" / "test_face.jpg"))
        if img is None:
            print("⚠ Foto de teste não encontrada, criando uma...")
            img = self._create_test_face()
        
        # Salva temporariamente
        temp_path = Path(__file__).parent / "temp_face.jpg"
        cv2.imwrite(str(temp_path), img)
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        with open(temp_path, "rb") as f:
            files = {"file": ("face.jpg", f, "image/jpeg")}
            response = requests.post(
                f"{API_URL}/api/v1/students/{self.student_id}/photos",
                files=files,
                headers=headers
            )
        
        temp_path.unlink()
        
        if response.status_code == 201:
            print("✓ Foto do aluno enviada")
            return True
        else:
            print(f"✗ Erro ao enviar foto: {response.status_code}")
            return False
    
    def create_camera(self):
        """4. Cadastra câmera de teste"""
        self.print_step("STEP 4: Cadastrar Câmera")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Usa o vídeo de teste como fonte
        video_path = Path(__file__).parent / "videos" / "test_video.mp4"
        
        camera_data = {
            "name": "Câmera Teste E2E",
            "rtsp_url": f"file://{video_path}",
            "location": "Teste",
            "enabled": True
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/cameras",
            json=camera_data,
            headers=headers
        )
        
        if response.status_code == 201:
            self.camera_id = response.json()["id"]
            print(f"✓ Câmera criada: ID {self.camera_id}")
            return True
        else:
            print(f"✗ Erro ao criar câmera: {response.status_code}")
            return False
    
    def start_streaming(self):
        """5. Inicia streaming"""
        self.print_step("STEP 5: Iniciar Streaming")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.post(
            f"{API_URL}/api/v1/cameras/{self.camera_id}/start",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ Streaming iniciado")
            return True
        else:
            print(f"✗ Erro ao iniciar streaming: {response.status_code}")
            return False
    
    def wait_for_detection(self, timeout: int = 60):
        """6. Aguarda detecção"""
        self.print_step("STEP 6: Aguardar Detecção")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        print(f"Aguardando detecção (timeout: {timeout}s)...")
        
        for i in range(timeout):
            response = requests.get(
                f"{API_URL}/api/v1/detections",
                params={"camera_id": self.camera_id, "limit": 1},
                headers=headers
            )
            
            if response.status_code == 200:
                detections = response.json()
                if detections:
                    print(f"✓ Detecção encontrada: {detections[0]}")
                    return True
            
            if i % 5 == 0:
                print(f"  Aguardando... {i}s")
            
            asyncio.sleep(1)
        
        print("✗ Timeout: Nenhuma detecção encontrada")
        return False
    
    def check_attendance(self):
        """7. Verifica registro de presença"""
        self.print_step("STEP 7: Verificar Presença")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        response = requests.get(
            f"{API_URL}/api/v1/attendance",
            params={"date": today, "student_id": self.student_id},
            headers=headers
        )
        
        if response.status_code == 200:
            records = response.json()
            if records:
                print(f"✓ Presença registrada: {records[0]}")
                return True
            else:
                print("✗ Nenhuma presença registrada")
                return False
        else:
            print(f"✗ Erro ao verificar presença: {response.status_code}")
            return False
    
    def check_notification(self):
        """8. Verifica notificação enviada"""
        self.print_step("STEP 8: Verificar Notificação")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(
            f"{API_URL}/api/v1/notifications",
            params={"student_id": self.student_id, "limit": 1},
            headers=headers
        )
        
        if response.status_code == 200:
            notifications = response.json()
            if notifications:
                print(f"✓ Notificação enviada: {notifications[0]}")
                return True
            else:
                print("⚠ Nenhuma notificação encontrada")
                return False
        else:
            print(f"✗ Erro ao verificar notificação: {response.status_code}")
            return False
    
    def cleanup(self):
        """9. Limpeza"""
        self.print_step("STEP 9: Limpeza")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Para streaming
        if self.camera_id:
            requests.post(
                f"{API_URL}/api/v1/cameras/{self.camera_id}/stop",
                headers=headers
            )
            print("✓ Streaming parado")
        
        print("✓ Limpeza concluída")
    
    def _create_test_face(self):
        """Cria uma imagem de teste com rosto simulado"""
        img = np.ones((480, 640, 3), dtype=np.uint8) * 200
        cv2.circle(img, (320, 240), 80, (200, 180, 150), -1)
        cv2.circle(img, (290, 220), 10, (0, 0, 0), -1)
        cv2.circle(img, (350, 220), 10, (0, 0, 0), -1)
        cv2.ellipse(img, (320, 260), (30, 15), 0, 0, 180, (0, 0, 0), 2)
        return img
    
    async def run(self):
        """Executa teste completo"""
        print("\n" + "="*60)
        print("🚀 TESTE E2E - GT-VISION SYSTEM")
        print("="*60)
        
        steps = [
            ("Login", self.login),
            ("Cadastrar Aluno", self.create_student),
            ("Upload Foto", self.upload_student_photo),
            ("Cadastrar Câmera", self.create_camera),
            ("Iniciar Streaming", self.start_streaming),
            ("Aguardar Detecção", lambda: self.wait_for_detection(60)),
            ("Verificar Presença", self.check_attendance),
            ("Verificar Notificação", self.check_notification),
        ]
        
        results = []
        
        try:
            for name, step_func in steps:
                result = step_func()
                results.append((name, result))
                
                if not result and name not in ["Verificar Notificação"]:
                    print(f"\n❌ Teste falhou em: {name}")
                    break
        
        finally:
            self.cleanup()
        
        # Relatório final
        self.print_step("RELATÓRIO FINAL")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for name, result in results:
            status = "✓" if result else "✗"
            print(f"{status} {name}")
        
        print(f"\n{'='*60}")
        print(f"Resultado: {passed}/{total} testes passaram")
        print(f"{'='*60}\n")
        
        return passed == total

if __name__ == "__main__":
    import numpy as np
    
    tester = SystemTester()
    success = asyncio.run(tester.run())
    
    sys.exit(0 if success else 1)
