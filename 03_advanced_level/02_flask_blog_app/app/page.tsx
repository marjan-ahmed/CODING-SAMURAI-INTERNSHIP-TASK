"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import {
  PlusCircle,
  Calendar,
  BookOpen,
  Sparkles,
  Coffee,
  Heart,
  MessageCircle,
  Share2,
  TrendingUp,
  Clock,
} from "lucide-react"

interface Article {
  id: number
  title: string
  content: string
  author: string
  created_at: string
}

export default function HomePage() {
  const [articles, setArticles] = useState<Article[]>([])
  const [user, setUser] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("token")
    if (token) {
      const userData = localStorage.getItem("user")
      if (userData) {
        setUser(JSON.parse(userData).username)
      }
    }

    // Fetch articles
    fetchArticles()
  }, [])

  const fetchArticles = async () => {
    try {
      const response = await fetch("/api/articles")
      if (response.ok) {
        const data = await response.json()
        setArticles(data.articles)
      }
    } catch (error) {
      console.error("Error fetching articles:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    setUser(null)
  }

  const getReadingTime = (content: string) => {
    const wordsPerMinute = 200
    const wordCount = content.split(" ").length
    const readingTime = Math.ceil(wordCount / wordsPerMinute)
    return readingTime
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="text-lg text-gray-600 font-medium">Loading amazing content...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50 shadow-sm">
        <div className="max-w-6xl mx-auto px-3 sm:px-4 py-3 sm:py-4">
          <div className="flex justify-between items-center">
            {/* Logo Section */}
            <div className="flex items-center space-x-2 sm:space-x-3">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg sm:rounded-xl flex items-center justify-center">
                <BookOpen className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
              </div>
              <div className="min-w-0">
                <h1 className="text-lg sm:text-xl md:text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent truncate">
                  ThoughtSpace
                </h1>
                <p className="text-xs text-gray-500 -mt-1 hidden xs:block">Where ideas come alive</p>
              </div>
            </div>

            {/* Navigation Section */}
            <div className="flex items-center gap-1 sm:gap-2 md:gap-3">
              {user ? (
                <>
                  {/* User Welcome - Hidden on mobile */}
                  <div className="hidden lg:flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-full">
                    <Avatar className="w-6 h-6">
                      <AvatarFallback className="text-xs bg-indigo-100 text-indigo-700">
                        {user.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm font-medium text-gray-700">Hey, {user}!</span>
                  </div>

                  {/* Mobile User Avatar - Visible only on mobile */}
                  <div className="flex lg:hidden items-center">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="text-sm bg-indigo-100 text-indigo-700">
                        {user.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </div>

                  {/* Write Button */}
                  <Link href="/create-article">
                    <Button
                      size="sm"
                      className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 px-2 sm:px-4"
                    >
                      <PlusCircle className="w-4 h-4 sm:mr-2" />
                      <span className="hidden sm:inline">Write</span>
                    </Button>
                  </Link>

                  {/* Logout Button */}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleLogout}
                    className="text-gray-600 hover:text-gray-900 px-2 sm:px-4"
                  >
                    <span className="hidden sm:inline">Logout</span>
                    <span className="sm:hidden text-xs">Exit</span>
                  </Button>
                </>
              ) : (
                <div className="flex gap-1 sm:gap-2">
                  {/* Sign In Button */}
                  <Link href="/login">
                    <Button variant="ghost" size="sm" className="text-gray-600 hover:text-gray-900 px-2 sm:px-4">
                      <span className="hidden sm:inline">Sign In</span>
                      <span className="sm:hidden text-xs">Login</span>
                    </Button>
                  </Link>

                  {/* Get Started Button */}
                  <Link href="/register">
                    <Button
                      size="sm"
                      className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 px-2 sm:px-4"
                    >
                      <span className="hidden sm:inline">Get Started</span>
                      <span className="sm:hidden text-xs">Join</span>
                    </Button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-16 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/60 backdrop-blur-sm rounded-full border border-gray-200/50 mb-6">
            <Sparkles className="w-4 h-4 text-indigo-500" />
            <span className="text-sm font-medium text-gray-700">Welcome to our community</span>
          </div>

          <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Discover Stories That
            <span className="block bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent">
              Inspire & Inform
            </span>
          </h2>

          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
            Join our community of writers and readers. Share your thoughts, discover new perspectives, and connect with
            like-minded individuals.
          </p>

          {!user && (
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register">
                <Button
                  size="lg"
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 px-8"
                >
                  Start Writing Today
                </Button>
              </Link>
              <Link href="/login">
                <Button size="lg" variant="outline" className="border-gray-300 hover:bg-gray-50 px-8">
                  Explore Articles
                </Button>
              </Link>
            </div>
          )}
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-8 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 text-center">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">{articles.length}+</h3>
              <p className="text-gray-600">Articles Published</p>
            </div>

            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 text-center">
              <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Growing</h3>
              <p className="text-gray-600">Community</p>
            </div>

            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 text-center">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                <Coffee className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Daily</h3>
              <p className="text-gray-600">Fresh Content</p>
            </div>
          </div>
        </div>
      </section>

      {/* Articles Section */}
      <main className="max-w-6xl mx-auto px-4 pb-16">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h3 className="text-3xl font-bold text-gray-900 mb-2">Latest Stories</h3>
            <p className="text-gray-600">Fresh perspectives from our community</p>
          </div>

          {user && (
            <Link href="/create-article">
              <Button variant="outline" className="hidden sm:flex items-center gap-2 border-gray-300 hover:bg-gray-50">
                <PlusCircle className="w-4 h-4" />
                New Story
              </Button>
            </Link>
          )}
        </div>

        {articles.length === 0 ? (
          <Card className="bg-white/60 backdrop-blur-sm border-gray-200/50 shadow-lg">
            <CardContent className="text-center py-16">
              <div className="w-16 h-16 bg-gradient-to-r from-gray-200 to-gray-300 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <BookOpen className="w-8 h-8 text-gray-500" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">No stories yet</h3>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                Be the pioneer! Share the first story and inspire others to join our growing community.
              </p>
              {user && (
                <Link href="/create-article">
                  <Button className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200">
                    <PlusCircle className="w-4 h-4 mr-2" />
                    Write First Story
                  </Button>
                </Link>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {articles.map((article, index) => (
              <Card
                key={article.id}
                className={`group bg-white/60 backdrop-blur-sm border-gray-200/50 shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 ${
                  index === 0 ? "lg:col-span-2" : ""
                }`}
              >
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between mb-3">
                    <Badge variant="secondary" className="bg-indigo-100 text-indigo-700 hover:bg-indigo-200">
                      Featured
                    </Badge>
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <Clock className="w-3 h-3" />
                      {getReadingTime(article.content)} min read
                    </div>
                  </div>

                  <CardTitle
                    className={`group-hover:text-indigo-600 transition-colors duration-200 ${
                      index === 0 ? "text-2xl md:text-3xl" : "text-xl"
                    }`}
                  >
                    {article.title}
                  </CardTitle>

                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    <div className="flex items-center gap-2">
                      <Avatar className="w-6 h-6">
                        <AvatarFallback className="text-xs bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700">
                          {article.author.charAt(0).toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <span className="font-medium">{article.author}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {new Date(article.created_at).toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                      })}
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="pt-0">
                  <p className={`text-gray-700 leading-relaxed mb-6 ${index === 0 ? "text-lg" : ""}`}>
                    {article.content.substring(0, index === 0 ? 300 : 150)}
                    {article.content.length > (index === 0 ? 300 : 150) && "..."}
                  </p>

                  <div className="flex items-center justify-between">
                    <Link href={`/article/${article.id}`}>
                      <Button
                        variant="ghost"
                        className="text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 p-0 h-auto font-semibold"
                      >
                        Continue reading →
                      </Button>
                    </Link>

                    <div className="flex items-center gap-3 text-gray-400">
                      <button className="hover:text-red-500 transition-colors duration-200">
                        <Heart className="w-4 h-4" />
                      </button>
                      <button className="hover:text-blue-500 transition-colors duration-200">
                        <MessageCircle className="w-4 h-4" />
                      </button>
                      <button className="hover:text-green-500 transition-colors duration-200">
                        <Share2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white/40 backdrop-blur-sm border-t border-gray-200/50 py-8 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
              <BookOpen className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-gray-900">ThoughtSpace</span>
          </div>
          <p className="text-gray-600 text-sm">Made with ❤️ for writers and readers everywhere</p>
        </div>
      </footer>
    </div>
  )
}
