"""
Teste rápido com webcam para validar detecção facial
"""
import cv2
import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

API_URL = "http://localhost:8000"

def test_webcam_detection():
    print("="*60)
    print("🎥 TESTE RÁPIDO - WEBCAM + DETECÇÃO")
    print("="*60)
    
    # 1. Login
    print("\n[1/4] Login...")
    response = requests.post(
        f"{API_URL}/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    
    if response.status_code != 200:
        print("❌ Erro no login")
        return False
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login OK")
    
    # 2. Criar câmera webcam
    print("\n[2/4] Criando câmera webcam...")
    camera_data = {
        "name": "Webcam Teste",
        "rtsp_url": "webcam://0",
        "location": "Teste Local",
        "enabled": True
    }
    
    response = requests.post(
        f"{API_URL}/api/v1/cameras",
        json=camera_data,
        headers=headers
    )
    
    if response.status_code != 201:
        print("❌ Erro ao criar câmera")
        return False
    
    camera_id = response.json()["id"]
    print(f"✓ Câmera criada: ID {camera_id}")
    
    # 3. Iniciar streaming
    print("\n[3/4] Iniciando streaming...")
    response = requests.post(
        f"{API_URL}/api/v1/cameras/{camera_id}/start",
        headers=headers
    )
    
    if response.status_code != 200:
        print("❌ Erro ao iniciar streaming")
        return False
    
    print("✓ Streaming iniciado")
    print("\n📹 Webcam ativa! Posicione seu rosto na frente da câmera...")
    print("⏱️  Aguardando 30 segundos para detecção...")
    
    # 4. Aguardar e verificar detecções
    print("\n[4/4] Monitorando detecções...")
    
    import time
    for i in range(30):
        time.sleep(1)
        
        response = requests.get(
            f"{API_URL}/api/v1/detections",
            params={"camera_id": camera_id, "limit": 5},
            headers=headers
        )
        
        if response.status_code == 200:
            detections = response.json()
            if detections:
                print(f"\n✓ {len(detections)} detecção(ões) encontrada(s)!")
                for det in detections[:3]:
                    print(f"  - Confiança: {det.get('confidence', 0):.2%}")
                break
        
        if i % 5 == 0:
            print(f"  Aguardando... {i}s")
    
    # Cleanup
    print("\n🧹 Parando streaming...")
    requests.post(
        f"{API_URL}/api/v1/cameras/{camera_id}/stop",
        headers=headers
    )
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO!")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_webcam_detection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
