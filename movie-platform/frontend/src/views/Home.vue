<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <h2>电影资讯</h2>
        <el-carousel height="300px">
          <el-carousel-item v-for="item in news" :key="item.id">
            <div class="carousel-content" :style="{ backgroundImage: `url(${item.image})` }">
              <h3>{{ item.title }}</h3>
            </div>
          </el-carousel-item>
        </el-carousel>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 30px;">
      <el-col :span="24">
        <h2>编辑精选</h2>
        <el-row :gutter="20">
          <el-col :span="6" v-for="movie in featuredMovies" :key="movie.id">
            <el-card :body-style="{ padding: '0px' }" @click="goToMovie(movie.id)" style="cursor: pointer;">
              <img :src="movie.poster_url" class="movie-poster" />
              <div style="padding: 14px;">
                <span>{{ movie.title }}</span>
                <div class="movie-rating">评分: {{ movie.rating || '暂无' }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 30px;">
      <el-col :span="24">
        <h2>热门推荐</h2>
        <el-row :gutter="20">
          <el-col :span="6" v-for="movie in popularMovies" :key="movie.id">
            <el-card :body-style="{ padding: '0px' }" @click="goToMovie(movie.id)" style="cursor: pointer;">
              <img :src="movie.poster_url" class="movie-poster" />
              <div style="padding: 14px;">
                <span>{{ movie.title }}</span>
                <div class="movie-rating">评分: {{ movie.rating || '暂无' }}</div>
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
import { useRouter } from 'vue-router'
import request from '@/api/request'

const router = useRouter()
const news = ref([
  { id: 1, title: '新片速递：奥本海默', image: 'https://via.placeholder.com/1200x300?text=Oppenheimer' },
  { id: 2, title: '暑期档票房破纪录', image: 'https://via.placeholder.com/1200x300?text=Summer+Box+Office' },
])
const featuredMovies = ref([])
const popularMovies = ref([])

const goToMovie = (id) => {
  router.push(`/movie/${id}`)
}

onMounted(async () => {
  try {
    // 获取推荐电影（这里简单调用电影列表，取前8部）
    const res = await request.get('/api/movies/?per_page=8')
    featuredMovies.value = res.data.slice(0, 4)
    popularMovies.value = res.data.slice(4, 8)
  } catch (error) {
    console.error(error)
  }
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}
.carousel-content {
  height: 100%;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: flex-end;
  padding: 20px;
  color: white;
}
.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
}
.movie-rating {
  font-size: 14px;
  color: #999;
  margin-top: 8px;
}
</style>