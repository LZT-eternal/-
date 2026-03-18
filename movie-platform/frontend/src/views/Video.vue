<template>
  <div class="video">
    <h2>视频</h2>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="热门" name="hot">
        <el-row :gutter="20">
          <el-col :span="6" v-for="video in videos.hot" :key="video.id">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="video.cover" style="width: 100%; height: 150px; object-fit: cover;" />
              <div style="padding: 10px;">
                <div>{{ video.title }}</div>
                <div style="font-size: 12px; color: #999;">{{ video.views }}次观看 · {{ video.duration }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="最新" name="new">
        <el-row :gutter="20">
          <el-col :span="6" v-for="video in videos.new" :key="video.id">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="video.cover" style="width: 100%; height: 150px; object-fit: cover;" />
              <div style="padding: 10px;">
                <div>{{ video.title }}</div>
                <div style="font-size: 12px; color: #999;">{{ video.views }}次观看 · {{ video.duration }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="预告" name="trailer">
        <el-row :gutter="20">
          <el-col :span="6" v-for="video in videos.trailer" :key="video.id">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="video.cover" style="width: 100%; height: 150px; object-fit: cover;" />
              <div style="padding: 10px;">
                <div>{{ video.title }}</div>
                <div style="font-size: 12px; color: #999;">{{ video.views }}次观看 · {{ video.duration }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="花絮" name="featurette">
        <el-row :gutter="20">
          <el-col :span="6" v-for="video in videos.featurette" :key="video.id">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="video.cover" style="width: 100%; height: 150px; object-fit: cover;" />
              <div style="padding: 10px;">
                <div>{{ video.title }}</div>
                <div style="font-size: 12px; color: #999;">{{ video.views }}次观看 · {{ video.duration }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="专访" name="interview">
        <el-row :gutter="20">
          <el-col :span="6" v-for="video in videos.interview" :key="video.id">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="video.cover" style="width: 100%; height: 150px; object-fit: cover;" />
              <div style="padding: 10px;">
                <div>{{ video.title }}</div>
                <div style="font-size: 12px; color: #999;">{{ video.views }}次观看 · {{ video.duration }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('hot')

// 模拟视频数据
const videos = {
  hot: [
    { id: 1, title: '热门视频1', cover: 'https://via.placeholder.com/300x150', views: 1200, duration: '3:45' },
    { id: 2, title: '热门视频2', cover: 'https://via.placeholder.com/300x150', views: 980, duration: '5:20' },
  ],
  new: [
    { id: 3, title: '最新视频1', cover: 'https://via.placeholder.com/300x150', views: 340, duration: '2:15' },
  ],
  trailer: [
    { id: 4, title: '预告片1', cover: 'https://via.placeholder.com/300x150', views: 560, duration: '1:30' },
  ],
  featurette: [
    { id: 5, title: '花絮1', cover: 'https://via.placeholder.com/300x150', views: 230, duration: '4:10' },
  ],
  interview: [
    { id: 6, title: '专访导演', cover: 'https://via.placeholder.com/300x150', views: 180, duration: '10:25' },
  ]
}
</script>