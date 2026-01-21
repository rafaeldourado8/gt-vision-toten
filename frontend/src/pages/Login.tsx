import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {Mail, Lock, Eye, EyeOff} from 'lucide-react';
import { Input } from "../components/common/Input";
import { Button } from "../components/common/Button";
import { authService } from "../services/auth";
import { useAuthStore } from "../stores/authStore";
import toast from "react-hot-toast";

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const setUser = useAuthStore((state) => state.setUser);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors = { email: "", password: "" };
    let isValid = true;

    if (!email) {
      newErrors.email = "Email é obrigatório";
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "Email inválido";
      isValid = false;
    }

    if (!password) {
      newErrors.password = "Senha é obrigatória";
      isValid = false;
    } else if (password.length < 6) {
      newErrors.password = "Senha deve ter no mínimo 6 caracteres";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);
    try {
      const response = await authService.login(email, password);
      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("user", JSON.stringify(response.user));
      
      if (rememberMe) {
        localStorage.setItem("remember_me", "true");
      }

      setUser(response.user);
      toast.success("Login realizado com sucesso!");
      navigate("/dashboard");
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Erro ao fazer login");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Image/Logo */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 to-blue-800 items-center justify-center p-12">
        <div className="text-center">
          <div className="mb-8">
            <div className="w-32 h-32 mx-auto bg-white rounded-2xl shadow-xl flex items-center justify-center">
              <span className="text-5xl">📹</span>
            </div>
          </div>
          <h1 className="text-4xl font-bold text-white mb-4">GT-Vision Toten</h1>
          <p className="text-xl text-blue-100">
            Sistema de Presença Escolar com Reconhecimento Facial
          </p>
          <div className="mt-12 space-y-4 text-left">
            <div className="flex items-center text-white">
              <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center mr-4">
                <span className="text-2xl">✓</span>
              </div>
              <div>
                <p className="font-semibold">Monitoramento em Tempo Real</p>
                <p className="text-sm text-blue-100">Detecção facial automática</p>
              </div>
            </div>
            <div className="flex items-center text-white">
              <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center mr-4">
                <span className="text-2xl">✓</span>
              </div>
              <div>
                <p className="font-semibold">Relatórios Completos</p>
                <p className="text-sm text-blue-100">Análise de presença detalhada</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md">
          <div className="text-center mb-8 lg:hidden">
            <div className="w-20 h-20 mx-auto bg-blue-600 rounded-xl shadow-lg flex items-center justify-center mb-4">
              <span className="text-3xl">📹</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">GT-Vision Toten</h1>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Bem-vindo</h2>
            <p className="text-gray-500 mb-8">Entre com suas credenciais para acessar o sistema</p>

            <form onSubmit={handleSubmit} className="space-y-6">
              <Input
                label="Email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={errors.email}
                icon={<Mail size={18} />}
              />

              <div>
                <Input
                  label="Senha"
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  error={errors.password}
                  icon={<Lock size={18} />}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-[38px] text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>

              <div className="flex items-center justify-between">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-600">Lembrar-me</span>
                </label>
                <a href="#" className="text-sm text-blue-600 hover:text-blue-700">
                  Esqueci minha senha
                </a>
              </div>

              <Button
                type="submit"
                variant="primary"
                className="w-full"
                disabled={loading}
              >
                {loading ? "Entrando..." : "Entrar"}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm text-gray-500">
              <p>Credenciais de teste:</p>
              <p className="font-mono text-xs mt-1">
                admin@gtvision.com / senha123
              </p>
            </div>
          </div>

          <p className="text-center text-sm text-gray-500 mt-6">
            © 2025 GT-Vision Toten. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </div>
  );
};
