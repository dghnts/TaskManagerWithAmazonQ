import React, { useState, useEffect, useCallback } from 'react';
import { 
  Typography, Box, Button, TextField, MenuItem, 
  FormControl, InputLabel, Select, Pagination,
  Alert, CircularProgress, InputAdornment, IconButton
} from '@mui/material';
import { Add, Search } from '@mui/icons-material';
import { taskAPI } from '../services/api';
import TaskCard from '../components/TaskCard';

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    category: '',
    priority: '',
    urgency: '',
    status: '',
    search: ''
  });
  const [searchInput, setSearchInput] = useState('');
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
    total_pages: 0
  });

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const params = {
        page: pagination.page,
        limit: pagination.limit,
        ...Object.fromEntries(
          Object.entries(filters).filter(([_, value]) => value !== '')
        )
      };
      
      const response = await taskAPI.getTasks(params);
      setTasks(response.data.tasks);
      setPagination(prev => ({
        ...prev,
        ...response.data.pagination
      }));
      setError(null);
    } catch (err) {
      setError('タスクの取得に失敗しました');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  }, [pagination.page, filters]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handleSearchSubmit = () => {
    setFilters(prev => ({ ...prev, search: searchInput }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handleSearchKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearchSubmit();
    }
  };

  const handlePageChange = (event, page) => {
    setPagination(prev => ({ ...prev, page }));
  };

  const handleTaskClick = (taskId) => {
    // タスク詳細画面への遷移（後で実装）
    console.log('Task clicked:', taskId);
  };

  const handleTaskEdit = (task) => {
    // タスク編集（後で実装）
    console.log('Edit task:', task);
  };

  const handleTaskDelete = async (taskId) => {
    if (window.confirm('このタスクを削除しますか？')) {
      try {
        await taskAPI.deleteTask(taskId);
        fetchTasks();
      } catch (err) {
        setError('タスクの削除に失敗しました');
      }
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          タスク一覧
        </Typography>
        <Button variant="contained" startIcon={<Add />}>
          新規タスク
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* フィルター */}
      <Box display="flex" gap={2} mb={3} flexWrap="wrap">
        <TextField
          label="検索"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          onKeyPress={handleSearchKeyPress}
          size="small"
          sx={{ minWidth: 200 }}
          placeholder="タスク名で検索..."
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={handleSearchSubmit}
                  size="small"
                  edge="end"
                >
                  <Search />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>カテゴリ</InputLabel>
          <Select
            value={filters.category}
            label="カテゴリ"
            onChange={(e) => handleFilterChange('category', e.target.value)}
          >
            <MenuItem value="">すべて</MenuItem>
            <MenuItem value="work">仕事</MenuItem>
            <MenuItem value="private">プライベート</MenuItem>
            <MenuItem value="study">学習</MenuItem>
            <MenuItem value="other">その他</MenuItem>
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>優先度</InputLabel>
          <Select
            value={filters.priority}
            label="優先度"
            onChange={(e) => handleFilterChange('priority', e.target.value)}
          >
            <MenuItem value="">すべて</MenuItem>
            <MenuItem value="high">高</MenuItem>
            <MenuItem value="medium">中</MenuItem>
            <MenuItem value="low">低</MenuItem>
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>緊急度</InputLabel>
          <Select
            value={filters.urgency}
            label="緊急度"
            onChange={(e) => handleFilterChange('urgency', e.target.value)}
          >
            <MenuItem value="">すべて</MenuItem>
            <MenuItem value="high">高</MenuItem>
            <MenuItem value="medium">中</MenuItem>
            <MenuItem value="low">低</MenuItem>
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>ステータス</InputLabel>
          <Select
            value={filters.status}
            label="ステータス"
            onChange={(e) => handleFilterChange('status', e.target.value)}
          >
            <MenuItem value="">すべて</MenuItem>
            <MenuItem value="not_started">未開始</MenuItem>
            <MenuItem value="in_progress">進行中</MenuItem>
            <MenuItem value="completed">完了</MenuItem>
            <MenuItem value="on_hold">保留</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* タスク一覧 */}
      {tasks.length === 0 ? (
        <Typography variant="body1" color="text.secondary" textAlign="center" mt={4}>
          タスクが見つかりません
        </Typography>
      ) : (
        <>
          {tasks.map(task => (
            <TaskCard
              key={task.id}
              task={task}
              onClick={handleTaskClick}
              onEdit={handleTaskEdit}
              onDelete={handleTaskDelete}
            />
          ))}
          
          {/* ページネーション */}
          {pagination.total_pages > 1 && (
            <Box display="flex" justifyContent="center" mt={3}>
              <Pagination
                count={pagination.total_pages}
                page={pagination.page}
                onChange={handlePageChange}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Box>
  );
}

export default TaskList;