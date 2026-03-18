<template>
  <div class="community">
    <h2>原创社区</h2>
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card v-for="post in posts" :key="post.id" style="margin-bottom: 20px;">
          <template #header>
            <div style="display: flex; justify-content: space-between;">
              <span><strong>{{ post.title }}</strong></span>
              <span style="color: #999;">{{ post.author }}</span>
            </div>
          </template>
          <div>{{ post.content }}</div>
          <div style="margin-top: 10px;">
            <el-button type="primary" link :icon="Star">点赞 {{ post.likes }}</el-button>
            <el-button type="primary" link :icon="ChatDotRound">评论 {{ post.comments }}</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>社区公告</template>
          <div>欢迎来到原创社区，大家可以自由发布影评和讨论。</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Star, ChatDotRound } from '@element-plus/icons-vue'

const posts = ref([
  { id: 1, title: '《奥本海默》观后感', author: '影迷小王', content: '这是一部震撼人心的电影...', likes: 45, comments: 12 },
  { id: 2, title: '暑期档电影推荐', author: '电影达人', content: '今年暑期档有很多好片，比如...', likes: 30, comments: 8 },
  { id: 3, title: '国产动画的崛起', author: '动漫迷', content: '近年来国产动画质量越来越高...', likes: 67, comments: 23 },
])
</script>