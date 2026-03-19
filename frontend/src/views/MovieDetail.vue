<template>
  <div class="movie-detail" v-if="movie">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-image :src="movie.poster_url" fit="cover" style="width: 100%; border-radius: 8px;" />
      </el-col>
      <el-col :span="16">
        <h1>{{ movie.title }} <span v-if="movie.original_title" style="font-size: 16px; color: #999;">({{ movie.original_title }})</span></h1>
        <div class="info-item">
          <span class="label">上映日期：</span>{{ movie.release_date }}
        </div>
        <div class="info-item">
          <span class="label">片长：</span>{{ movie.duration }} 分钟
        </div>
        <div class="info-item">
          <span class="label">语言：</span>{{ movie.language }}
        </div>
        <div class="info-item">
          <span class="label">国家/地区：</span>{{ movie.country }}
        </div>
        <div class="info-item">
          <span class="label">类型：</span>
          <el-tag v-for="genre in movie.genres" :key="genre.id" size="small" style="margin-right: 5px;">{{ genre.name }}</el-tag>
        </div>
        <div class="info-item">
          <span class="label">评分：</span>{{ movie.rating || '暂无' }}
        </div>
        <div class="info-item">
          <span class="label">简介：</span>{{ movie.description }}
        </div>
        <div style="margin-top: 20px;">
          <el-button type="primary" @click="toggleFavorite" :loading="favoriteLoading">
            {{ isFavorite ? '取消收藏' : '收藏' }}
          </el-button>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 40px;">
      <el-col :span="24">
        <h3>影人</h3>
        <el-row :gutter="20">
          <el-col :span="4" v-for="celeb in movie.celebrities" :key="celeb.id">
            <el-card :body-style="{ padding: '10px' }">
              <el-avatar :src="celeb.photo_url" :size="80" shape="square" />
              <div style="text-align: center; margin-top: 10px;">
                <strong>{{ celeb.name }}</strong>
                <div>{{ celeb.role }} {{ celeb.character ? '/' + celeb.character : '' }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 40px;">
      <el-col :span="24">
        <h3>推荐电影</h3>
        <el-row :gutter="20">
          <el-col :span="4" v-for="rec in recommendations" :key="rec.id">
            <el-card :body-style="{ padding: '0px' }" @click="goToMovie(rec.id)" style="cursor: pointer;">
              <img :src="rec.poster_url" style="width: 100%; height: 200px; object-fit: cover;" />
              <div style="padding: 10px;">
                <div>{{ rec.title }}</div>
                <div style="font-size: 12px; color: #999;">评分: {{ rec.rating || '暂无' }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()
const movieId = route.params.id
const movie = ref(null)
const isFavorite = ref(false)
const favoriteLoading = ref(false)
const recommendations = ref([])

const fetchMovie = async () => {
  try {
    const res = await request.get(`/api/movies/${movieId}`)
    movie.value = res
    // 获取推荐（这里简单用同类型的，实际可调用推荐接口）
    await fetchRecommendations()
  } catch (error) {
    console.error(error)
  }
}

const fetchRecommendations = async () => {
  try {
    const res = await request.get('/api/recommendations/user')
    recommendations.value = res.slice(0, 6)
  } catch (error) {
    console.error(error)
  }
}

const checkFavorite = async () => {
  try {
    const res = await request.get('/api/movies/favorites')
    isFavorite.value = res.some(f => f.id === parseInt(movieId))
  } catch (error) {
    console.error(error)
  }
}

const toggleFavorite = async () => {
  favoriteLoading.value = true
  try {
    const res = await request.post(`/api/movies/${movieId}/favorite`)
    isFavorite.value = res.favorite
    ElMessage.success(isFavorite.value ? '收藏成功' : '已取消收藏')
  } catch (error) {
    console.error(error)
  } finally {
    favoriteLoading.value = false
  }
}

const goToMovie = (id) => {
  router.push(`/movie/${id}`)
}

onMounted(() => {
  fetchMovie()
  checkFavorite()
})
</script>

<style scoped>
.movie-detail {
  max-width: 1200px;
  margin: 0 auto;
}
.info-item {
  margin-bottom: 10px;
}
.label {
  font-weight: bold;
  width: 80px;
  display: inline-block;
}
</style>