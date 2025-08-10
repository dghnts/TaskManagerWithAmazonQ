import axios from 'axios';

// APIクライアントの設定
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// レスポンスインターセプター（エラーハンドリング）
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// タスク関連のAPI
export const taskAPI = {
  // タスク一覧取得
  getTasks: (params = {}) => apiClient.get('/tasks', { params }),
  
  // タスク詳細取得
  getTask: (id) => apiClient.get(`/tasks/${id}`),
  
  // タスク作成
  createTask: (data) => apiClient.post('/tasks', data),
  
  // タスク更新
  updateTask: (id, data) => apiClient.put(`/tasks/${id}`, data),
  
  // タスク削除
  deleteTask: (id) => apiClient.delete(`/tasks/${id}`),
  
  // マトリックス表示データ取得
  getMatrixData: () => apiClient.get('/tasks/matrix'),
  
  // カレンダー表示データ取得
  getCalendarData: (year, month) => apiClient.get('/tasks/calendar', {
    params: { year, month }
  }),
};

// サブタスク関連のAPI
export const subtaskAPI = {
  // サブタスク一覧取得
  getSubtasks: (taskId) => apiClient.get(`/tasks/${taskId}/subtasks`),
  
  // サブタスク作成
  createSubtask: (taskId, data) => apiClient.post(`/tasks/${taskId}/subtasks`, data),
  
  // サブタスク更新
  updateSubtask: (id, data) => apiClient.put(`/subtasks/${id}`, data),
  
  // サブタスク削除
  deleteSubtask: (id) => apiClient.delete(`/subtasks/${id}`),
};

// コメント関連のAPI
export const commentAPI = {
  // コメント一覧取得
  getComments: (taskId) => apiClient.get(`/tasks/${taskId}/comments`),
  
  // コメント作成
  createComment: (taskId, data) => apiClient.post(`/tasks/${taskId}/comments`, data),
  
  // コメント削除
  deleteComment: (id) => apiClient.delete(`/comments/${id}`),
};

export default apiClient;