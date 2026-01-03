import React, { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/common/Card'
import { Button } from '@/components/common/Button'
import { Input } from '@/components/common/Input'
import { User, Mail, Lock, Loader2, ArrowRight, Database } from 'lucide-react'

export function LoginPage() {
    const { login, register } = useAuth()
    const [isLogin, setIsLogin] = useState(true)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    // Form state
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            if (isLogin) {
                // Log in allows username OR email, but our UI has separate fields?
                // Actually backend supports `username_or_email`.
                // Let's simplified the UI for login to just use "username" state as the identifier
                // But wait, the registration needs both.
                // Let's use `email` or `username` based on what the user types if we had a single field,
                // but for registration we need distinct fields.

                // For login, we will use the `username` field as the identifier (username or email).
                await login({ username: username, password })
                // Navigation is handled in AuthContext or triggered here? 
                // AuthContext sets user/token. redirection usually happens in App or here.
                window.location.hash = 'dashboard'
            } else {
                await register({ username, email, password })
                window.location.hash = 'dashboard'
            }
        } catch (err: any) {
            setError(err.message || '操作失败，请重试')
        } finally {
            setLoading(false)
        }
    }

    const toggleMode = () => {
        setIsLogin(!isLogin)
        setError('')
        setUsername('')
        setEmail('')
        setPassword('')
    }

    return (
        <div className="flex min-h-screen w-full items-center justify-center bg-background p-4 relative overflow-hidden">
            {/* Background decoration */}
            <div className="absolute top-[-20%] right-[-10%] h-[600px] w-[600px] rounded-full bg-primary/5 blur-[100px]" />
            <div className="absolute bottom-[-20%] left-[-10%] h-[600px] w-[600px] rounded-full bg-blue-500/5 blur-[100px]" />

            <div className="w-full max-w-md animate-in fade-in zoom-in-95 duration-500">
                <div className="mb-8 text-center">
                    <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
                        <Database className="h-8 w-8 text-primary" />
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">Bears PanguCreate</h1>
                    <p className="mt-2 text-muted-foreground">企业级海量测试数据生成平台</p>
                </div>

                <Card className="border-primary/10 shadow-xl backdrop-blur-sm bg-card/50">
                    <CardHeader>
                        <CardTitle>{isLogin ? '欢迎回来' : '创建账号'}</CardTitle>
                        <CardDescription>
                            {isLogin ? '请输入您的账号密码进行登录' : '填写以下信息开启您的数据生成之旅'}
                        </CardDescription>
                    </CardHeader>

                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {error && (
                                <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                                    {error}
                                </div>
                            )}

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    {isLogin ? '账号 / 邮箱' : '用户名'}
                                </label>
                                <div className="relative">
                                    <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        type="text"
                                        placeholder={isLogin ? "请输入用户名或邮箱" : "请输入用户名"}
                                        className="pl-9"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        required
                                    />
                                </div>
                            </div>

                            {!isLogin && (
                                <div className="space-y-2 animate-in slide-in-from-top-2 duration-300">
                                    <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                        邮箱地址
                                    </label>
                                    <div className="relative">
                                        <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                        <Input
                                            type="email"
                                            placeholder="name@example.com"
                                            className="pl-9"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>
                            )}

                            <div className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                        密码
                                    </label>
                                    {isLogin && (
                                        <a href="#" className="text-xs text-primary hover:underline">
                                            忘记密码？
                                        </a>
                                    )}
                                </div>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        type="password"
                                        placeholder="••••••••"
                                        className="pl-9"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                        minLength={6}
                                    />
                                </div>
                            </div>

                            <Button
                                type="submit"
                                className="w-full"
                                disabled={loading}
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        {isLogin ? '登录中...' : '注册中...'}
                                    </>
                                ) : (
                                    <>
                                        {isLogin ? '立即登录' : '立即注册'}
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </>
                                )}
                            </Button>
                        </form>
                    </CardContent>

                    <CardFooter>
                        <div className="w-full text-center text-sm text-muted-foreground">
                            {isLogin ? '还没有账号？' : '已有账号？'}
                            <button
                                type="button"
                                onClick={toggleMode}
                                className="ml-1 font-medium text-primary hover:underline"
                            >
                                {isLogin ? '去注册' : '去登录'}
                            </button>
                        </div>
                    </CardFooter>
                </Card>

                <div className="mt-8 text-center text-xs text-muted-foreground">
                    &copy; 2026 Bears PanguCreate. All rights reserved.
                </div>
            </div>
        </div>
    )
}
