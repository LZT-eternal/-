<template>
  <div>
    <el-page-header :icon="null" title="电影管理">
      <template #content>
        <span class="text-large font-600 mr-3"> 电影列表 </span>
      </template>
      <template #extra>
        <el-button type="primary" @click="handleAdd">新增电影</el-button>
      </template>
    </el-page-header>

    <el-table :data="movies" border stripe style="margin-top: 20px">
      <el-table-column prop="movie_id" label="ID" width="60" />
      <el-table-column prop="title" label="片名" />
      <el-table-column prop="release_date" label="上映日期" width="120" />
      <el-table-column prop="country" label="国家" width="100" />
      <el-table-column prop="rating" label="评分" width="80" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="片名">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
        <el-form-item label="上映日期">
          <el-date-picker v-model="form.release_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="片长">
          <el-input v-model="form.duration" type="number" />
        </el-form-item>
        <el-form-item label="语言">
          <el-input v-model="form.language" />
        </el-form-item>
        <el-form-item label="国家">
          <el-input v-model="form.country" />
        </el-form-item>
        <el-form-item label="海报URL">
          <el-input v-model="form.poster_url" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveMovie">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../api/request'

const movies = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const form = ref({})

const fetchMovies = async () => {
  movies.value = await request.get('/api/movies')
}
onMounted(fetchMovies)

const handleAdd = () => {
  dialogTitle.value = '新增电影'
  form.value = {}
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑电影'
  form.value = { ...row }
  dialogVisible.value = true
}

const saveMovie = async () => {
  if (form.value.movie_id) {
    await request.put(`/api/movies/${form.value.movie_id}`, form.value)
    ElMessage.success('更新成功')
  } else {
    await request.post('/api/movies', form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  fetchMovies()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该电影吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await request.delete(`/api/movies/${row.movie_id}`)
    ElMessage.success('删除成功')
    fetchMovies()
  })
}
</script>