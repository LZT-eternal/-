<template>
  <div>
    <h2>票房趋势分析</h2>
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <div ref="chart" style="height: 400px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import request from '../api/request'

const chart = ref(null)

onMounted(async () => {
  const data = await request.get('/api/boxoffice/trend')  // 需要实现该接口
  const myChart = echarts.init(chart.value)
  myChart.setOption({
    title: { text: '近30天票房走势' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: data.dates },
    yAxis: { type: 'value' },
    series: [{ name: '票房', type: 'line', data: data.amounts }]
  })
})
</script>