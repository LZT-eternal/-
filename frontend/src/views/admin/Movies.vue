<template>
  <div class="admin-movies">
    <h2>电影管理</h2>
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-input v-model="searchForm.title" placeholder="片名" clearable @clear="fetchData" @keyup.enter="fetchData" />
      </el-col>
      <el-col :span="4">
        <el-select v-model="searchForm.genre_id" placeholder="类型" clearable @change="fetchData">
          <el-option v-for="g in genres" :key="g.id" :label="g.name" :value="g.id" />
        </el-select>
      </el-col>
      <el-col :span="4">
        <el-select v-model="searchForm.year" placeholder="年份" clearable @change="fetchData">
          <el-option v-for="y in years" :key="y" :label="y" :value="y" />
        </el-select>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" @click="fetchData">查询</el-button>
        <el-button type="success" @click="openDialog">新增</el-button>
      </el-col>
    </el-row>

    <el-table :data="movies" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="片名" />
      <el-table-column prop="release_date" label="上映日期" width="120" />
      <el-table-column prop="rating" label="评分" width="80" />
      <el-table-column label="类型" width="150">
        <template #default="{ row }">
          <el-tag v-for="g in row.genres" :key="g.id" size="small" style="margin-right: 3px;">{{ g.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_blocked" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_blocked ? 'danger' : 'success'">{{ row.is_blocked ? '已屏蔽' : '正常' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" @click="openDialog(row)">编辑</el-button>
          <el-button size="small" :type="row.is_blocked ? 'success' : 'warning'" @click="toggleBlock(row)">
            {{ row.is_blocked ? '解除屏蔽' : '屏蔽' }}
          </el-button>
          <el-button size="small" type="danger" @click="confirmDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="page"
      v-model:page-size="perPage"
      :total="total"
      :page-sizes="[10, 20, 50]"
      layout="total, sizes, prev, pager, next"
      @size-change="fetchData"
      @current-change="fetchData"
      style="margin-top: 20px;"
    />

    <!-- 新增/编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="片名" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="原名" prop="original_title">
          <el-input v-model="form.original_title" />
        </el-form-item>
        <el-form-item label="简介" prop="description">
          <el-input v-model="form.description" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="上映日期" prop="release_date">
          <el-date-picker v-model="form.release_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="片长(分钟)" prop="duration">
          <el-input-number v-model="form.duration" :min="0" />
        </el-form-item>
        <el-form-item label="语言" prop="language">
          <el-input v-model="form.language" />
        </el-form-item>
        <el-form-item label="国家" prop="country">
          <el-input v-model="form.country" />
        </el-form-item>
        <el-form-item label="海报URL" prop="poster_url">
          <el-input v-model="form.poster_url" />
        </el-form-item>
        <el-form-item label="评分" prop="rating">
          <el-input-number v-model="form.rating" :min="0" :max="10" :step="0.1" />
        </el-form-item>
        <el-form-item label="类型" prop="genre_ids">
          <el-select v-model="form.genre_ids" multiple filterable>
            <el-option v-for="g in genres" :key="g.id" :label="g.name" :value="g.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="屏蔽" prop="is_blocked">
          <el-switch v-model="form.is_blocked" />
        </el-form-item>
        <el-form-item label="置顶" prop="is_sticky">
          <el-switch v-model="form.is_sticky" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/request'

const movies = ref([])
const total = ref(0)
const page = ref(1)
const perPage = ref(10)
const genres = ref([])
const years = ref([])

const searchForm = reactive({
  title: '',
  genre_id: null,
  year: null
})

const fetchGenres = async () => {
  try {
    const res = await request.get('/api/movies/genres')
    genres.value = res
  } catch (error) {
    console.error(error)
  }
}

const fetchYears = async () => {
  try {
    const res = await request.get('/api/movies/years')
    years.value = res
  } catch (error) {
    console.error(error)
  }
}

const fetchData = async () => {
  try {
    const params = {
      page: page.value,
      per_page: perPage.value,
      ...searchForm
    }
    if (!params.title) delete params.title
    if (!params.genre_id) delete params.genre_id
    if (!params.year) delete params.year
    const res = await request.get('/api/movies/', { params })
    movies.value = res.data
    total.value = res.total
  } catch (error) {
    console.error(error)
  }
}

const dialogVisible = ref(false)
const dialogTitle = ref('新增电影')
const formRef = ref(null)
const saving = ref(false)
const form = reactive({
  id: null,
  title: '',
  original_title: '',
  description: '',
  release_date: '',
  duration: 90,
  language: '',
  country: '',
  poster_url: '',
  rating: 0,
  genre_ids: [],
  is_blocked: false,
  is_sticky: false
})

const rules = {
  title: [{ required: true, message: '请输入片名', trigger: 'blur' }]
}

const openDialog = (row) => {
  if (row) {
    dialogTitle.value = '编辑电影'
    Object.assign(form, row)
    form.release_date = row.release_date || ''
    form.genre_ids = row.genres ? row.genres.map(g => g.id) : []
  } else {
    dialogTitle.value = '新增电影'
    Object.keys(form).forEach(key => {
      if (key === 'id') form.id = null
      else if (key === 'duration') form.duration = 90
      else if (key === 'rating') form.rating = 0
      else if (key === 'is_blocked') form.is_blocked = false
      else if (key === 'is_sticky') form.is_sticky = false
      else form[key] = ''
    })
    form.genre_ids = []
  }
  dialogVisible.value = true
}

const save = async () => {
  await formRef.value.validate()
  saving.value = true
  try {
    if (form.id) {
      await request.put(`/api/movies/${form.id}`, form)
      ElMessage.success('更新成功')
    } else {
      await request.post('/api/movies/', form)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error(error)
  } finally {
    saving.value = false
  }
}

const toggleBlock = async (row) => {
  try {
    const newBlocked = !row.is_blocked
    await request.put(`/api/movies/${row.id}`, { is_blocked: newBlocked })
    row.is_blocked = newBlocked
    ElMessage.success(newBlocked ? '已屏蔽' : '已解除屏蔽')
  } catch (error) {
    console.error(error)
  }
}

const confirmDelete = (row) => {
  ElMessageBox.confirm(`确定删除电影《${row.title}》吗？`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request.delete(`/api/movies/${row.id}`)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      console.error(error)
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchGenres()
  fetchYears()
  fetchData()
})
</script>