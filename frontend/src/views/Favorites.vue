<template>
  <div class="favorites">
    <h2>我的收藏</h2>
    <el-row :gutter="20">
      <el-col :span="6" v-for="movie in favorites" :key="movie.id">
        <el-card :body-style="{ padding: '0px' }" style="margin-bottom: 20px;">
          <img :src="movie.poster_url" style="width: 100%; height: 250px; object-fit: cover;" @click="goToMovie(movie.id)" />
          <div style="padding: 14px;">
            <div @click="goToMovie(movie.id)" style="cursor: pointer;">{{ movie.title }}</div>
            <div style="font-size: 14px; color: #999;">评分: {{ movie.rating || '暂无' }}</div>
            <el-button type="danger" size="small" @click="removeFavorite(movie.id)" style="margin-top: 10px;">取消收藏</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="favorites.length === 0" description="暂无收藏" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const router = useRouter()
const favorites = ref([])

const fetchFavorites = async () => {
  try {
    const res = await request.get('/api/movies/favorites')
    favorites.value = res
  } catch (error) {
    console.error(error)
  }
}

const removeFavorite = async (movieId) => {
  try {
    await request.post(`/api/movies/${movieId}/favorite`)
    favorites.value = favorites.value.filter(m => m.id !== movieId)
    ElMessage.success('已取消收藏')
  } catch (error) {
    console.error(error)
  }
}

const goToMovie = (id) => {
  router.push(`/movie/${id}`)
}

onMounted(fetchFavorites)
</script>