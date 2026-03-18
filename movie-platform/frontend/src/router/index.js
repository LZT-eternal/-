import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'
import AdminLayout from '@/components/AdminLayout.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'
import MovieDetail from '@/views/MovieDetail.vue'
import Community from '@/views/Community.vue'
import Video from '@/views/Video.vue'
import Favorites from '@/views/Favorites.vue'
import Visualization from '@/views/Visualization.vue'
import AdminMovies from '@/views/admin/Movies.vue'
import AdminCelebrities from '@/views/admin/Celebrities.vue'
import AdminUsers from '@/views/admin/Users.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Home',
        component: Home
      },
      {
        path: 'movie/:id',
        name: 'MovieDetail',
        component: MovieDetail
      },
      {
        path: 'community',
        name: 'Community',
        component: Community
      },
      {
        path: 'video',
        name: 'Video',
        component: Video
      },
      {
        path: 'favorites',
        name: 'Favorites',
        component: Favorites,
        meta: { requiresAuth: true }
      },
      {
        path: 'visualization',
        name: 'Visualization',
        component: Visualization
      }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        redirect: '/admin/movies'
      },
      {
        path: 'movies',
        name: 'AdminMovies',
        component: AdminMovies
      },
      {
        path: 'celebrities',
        name: 'AdminCelebrities',
        component: AdminCelebrities
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userStr = localStorage.getItem('user')
  let user = null
  if (userStr) {
    try {
      user = JSON.parse(userStr)
    } catch (e) {
      user = null
    }
  }

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token || !user) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }

  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (!user || user.role !== 'admin') {
      next({ name: 'Home' })
      return
    }
  }

  next()
})

export default router