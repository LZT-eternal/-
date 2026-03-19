<template>
  <div class="admin-celebrities">
    <h2>影人管理</h2>
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-input v-model="searchForm.name" placeholder="姓名" clearable @clear="fetchData" @keyup.enter="fetchData" />
      </el-col>
      <el-col :span="4">
        <el-input v-model="searchForm.nationality" placeholder="国籍" clearable @clear="fetchData" @keyup.enter="fetchData" />
      </el-col>
      <el-col :span="4">
        <el-button type="primary" @click="fetchData">查询</el-button>
        <el-button type="success" @click="openDialog">新增</el-button>
      </el-col>
    </el-row>

    <el-table :data="celebrities" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="照片" width="80">
        <template #default="{ row }">
          <el-avatar :src="row.photo_url" shape="square" :size="50" />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别" width="60" />
      <el-table-column prop="birth_date" label="出生日期" width="120" />
      <el-table-column prop="nationality" label="国籍" />
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
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="form.gender">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="出生日期" prop="birth_date">
          <el-date-picker v-model="form.birth_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="国籍" prop="nationality">
          <el-input v-model="form.nationality" />
        </el-form-item>
        <el-form-item label="简介" prop="biography">
          <el-input v-model="form.biography" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="照片URL" prop="photo_url">
          <el-input v-model="form.photo_url" />
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

const celebrities = ref([])
const total = ref(0)
const page = ref(1)
const perPage = ref(10)

const searchForm = reactive({
  name: '',
  nationality: ''
})

const fetchData = async () => {
  try {
    const params = {
      page: page.value,
      per_page: perPage.value,
      ...searchForm
    }
    if (!params.name) delete params.name
    if (!params.nationality) delete params.nationality
    const res = await request.get('/api/celebrities/', { params })
    celebrities.value = res.data
    total.value = res.total
  } catch (error) {
    console.error(error)
  }
}

const dialogVisible = ref(false)
const dialogTitle = ref('新增影人')
const formRef = ref(null)
const saving = ref(false)
const form = reactive({
  id: null,
  name: '',
  gender: '',
  birth_date: '',
  nationality: '',
  biography: '',
  photo_url: '',
  is_blocked: false,
  is_sticky: false
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
}

const openDialog = (row) => {
  if (row) {
    dialogTitle.value = '编辑影人'
    Object.assign(form, row)
    form.birth_date = row.birth_date || ''
  } else {
    dialogTitle.value = '新增影人'
    Object.keys(form).forEach(key => {
      if (key === 'id') form.id = null
      else if (key === 'is_blocked' || key === 'is_sticky') form[key] = false
      else form[key] = ''
    })
  }
  dialogVisible.value = true
}

const save = async () => {
  await formRef.value.validate()
  saving.value = true
  try {
    if (form.id) {
      await request.put(`/api/celebrities/${form.id}`, form)
      ElMessage.success('更新成功')
    } else {
      await request.post('/api/celebrities/', form)
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
    await request.put(`/api/celebrities/${row.id}`, { is_blocked: newBlocked })
    row.is_blocked = newBlocked
    ElMessage.success(newBlocked ? '已屏蔽' : '已解除屏蔽')
  } catch (error) {
    console.error(error)
  }
}

const confirmDelete = (row) => {
  ElMessageBox.confirm(`确定删除影人 ${row.name} 吗？`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request.delete(`/api/celebrities/${row.id}`)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      console.error(error)
    }
  }).catch(() => {})
}

onMounted(fetchData)
</script>