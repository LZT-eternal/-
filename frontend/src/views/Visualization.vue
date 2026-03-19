<template>
  <div class="visualization">
    <h2>数据可视化</h2>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>近30天票房趋势</template>
          <div ref="trendChart" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>地区票房分布</template>
          <div ref="regionChart" style="height: 400px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>电影类型占比</template>
          <div ref="genreChart" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import request from '@/api/request'

const trendChart = ref(null)
const regionChart = ref(null)
const genreChart = ref(null)

let trendInstance, regionInstance, genreInstance

const fetchData = async () => {
  try {
    // 票房趋势
    const trendRes = await request.get('/api/boxoffice/trend?days=30')
    const dates = trendRes.map(item => item.date)
    const amounts = trendRes.map(item => item.amount)
    trendInstance.setOption({
      xAxis: { data: dates },
      series: [{ data: amounts, type: 'line', smooth: true }]
    })

    // 地区分布
    const regionRes = await request.get('/api/boxoffice/region')
    const regions = regionRes.map(item => item.region)
    const regionAmounts = regionRes.map(item => item.amount)
    regionInstance.setOption({
      xAxis: { data: regions },
      series: [{ data: regionAmounts, type: 'bar' }]
    })

    // 类型占比（模拟数据，因为没有专门接口，这里从电影统计中获取）
    const moviesRes = await request.get('/api/movies/?per_page=100')
    const genresCount = {}
    moviesRes.data.forEach(movie => {
      movie.genres.forEach(g => {
        genresCount[g.name] = (genresCount[g.name] || 0) + 1
      })
    })
    const genreNames = Object.keys(genresCount)
    const genreValues = Object.values(genresCount)
    genreInstance.setOption({
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        data: genreNames.map((name, index) => ({ name, value: genreValues[index] }))
      }]
    })
  } catch (error) {
    console.error('获取图表数据失败', error)
    // 使用模拟数据
    trendInstance.setOption({
      xAxis: { data: ['2025-03-01', '2025-03-02', '2025-03-03'] },
      series: [{ data: [120, 200, 150], type: 'line' }]
    })
    regionInstance.setOption({
      xAxis: { data: ['北京', '上海', '广州'] },
      series: [{ data: [300, 450, 200], type: 'bar' }]
    })
    genreInstance.setOption({
      series: [{
        type: 'pie',
        data: [
          { name: '动作', value: 30 },
          { name: '喜剧', value: 25 },
          { name: '爱情', value: 20 },
          { name: '科幻', value: 15 },
          { name: '其他', value: 10 }
        ]
      }]
    })
  }
}

onMounted(() => {
  trendInstance = echarts.init(trendChart.value)
  regionInstance = echarts.init(regionChart.value)
  genreInstance = echarts.init(genreChart.value)
  fetchData()
})
</script>