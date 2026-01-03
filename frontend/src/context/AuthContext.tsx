import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { User, login as apiLogin, register as apiRegister, getCurrentUser } from '../lib/api'

interface AuthContextType {
    user: User | null
    token: string | null
    isAuthenticated: boolean
    isLoading: boolean
    login: (data: { username?: string, email?: string, password: string }) => Promise<void>
    register: (data: { username: string, email: string, password: string }) => Promise<void>
    logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null)
    const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'))
    const [isLoading, setIsLoading] = useState(true)

    // 初始化检查 token
    useEffect(() => {
        const initAuth = async () => {
            const storedToken = localStorage.getItem('access_token')
            if (storedToken) {
                try {
                    const user = await getCurrentUser(storedToken)
                    setUser(user)
                    setToken(storedToken)
                } catch (error) {
                    console.error('Token invalid or expired:', error)
                    logout()
                }
            }
            setIsLoading(false)
        }

        initAuth()
    }, [])

    const login = async (data: { username?: string, email?: string, password: string }) => {
        const response = await apiLogin(data)
        const { access_token, user } = response.data

        localStorage.setItem('access_token', access_token)
        if (response.data.refresh_token) {
            localStorage.setItem('refresh_token', response.data.refresh_token)
        }

        setToken(access_token)
        setUser(user)
    }

    const register = async (data: { username: string, email: string, password: string }) => {
        const response = await apiRegister(data)
        const { access_token, user } = response.data

        localStorage.setItem('access_token', access_token)
        if (response.data.refresh_token) {
            localStorage.setItem('refresh_token', response.data.refresh_token)
        }

        setToken(access_token)
        setUser(user)
    }

    const logout = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        setToken(null)
        setUser(null)
        // Optional: Redirect to login page if currently on a protected page
        window.location.hash = 'login'
    }

    return (
        <AuthContext.Provider value={{
            user,
            token,
            isAuthenticated: !!user,
            isLoading,
            login,
            register,
            logout
        }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context
}
