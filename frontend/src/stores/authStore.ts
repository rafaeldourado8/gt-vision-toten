import { create } from "zustand";
import { User } from "../types";
import { authService } from "../services/auth";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: authService.getUser(),
  isAuthenticated: authService.isAuthenticated(),
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  logout: () => {
    authService.logout();
    set({ user: null, isAuthenticated: false });
  },
}));
