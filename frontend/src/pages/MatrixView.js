import React, { useState, useEffect } from 'react';
import { 
  Typography, Box, Alert, CircularProgress, 
  Card, CardContent, Grid
} from '@mui/material';
import { taskAPI } from '../services/api';
import MatrixGrid from '../components/MatrixGrid';

function MatrixView() {
  const [matrixData, setMatrixData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMatrixData = async () => {
    try {
      setLoading(true);
      const response = await taskAPI.getMatrixData();
      setMatrixData(response.data);
      setError(null);
    } catch (err) {
      setError('マトリックスデータの取得に失敗しました');
      console.error('Error fetching matrix data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatrixData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        アイゼンハワーマトリックス
      </Typography>
      
      <Typography variant="body1" color="text.secondary" mb={3}>
        タスクを重要度と緊急度で分類して表示します
      </Typography>

      {/* サマリー情報 */}
      {matrixData?.summary && (
        <Grid container spacing={2} mb={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="primary">
                  {matrixData.summary.total_tasks}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  総タスク数
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="error">
                  {matrixData.summary.by_quadrant?.quadrant_1 || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  第1象限（重要・緊急）
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="warning">
                  {matrixData.summary.by_quadrant?.quadrant_2 || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  第2象限（重要・非緊急）
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="info">
                  {(matrixData.summary.by_quadrant?.quadrant_3 || 0) + 
                   (matrixData.summary.by_quadrant?.quadrant_4 || 0)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  第3・4象限
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* マトリックスグリッド */}
      {matrixData?.matrix && (
        <MatrixGrid matrixData={matrixData.matrix} />
      )}
      
      {/* アドバイス */}
      <Box mt={4}>
        <Typography variant="h6" gutterBottom>
          タスク管理のアドバイス
        </Typography>
        <Typography variant="body2" color="text.secondary">
          ・ 第1象限（重要・緊急）: すぐに実行しましょう<br/>
          ・ 第2象限（重要・非緊急）: 計画を立てて実行しましょう<br/>
          ・ 第3象限（非重要・緊急）: 他人に任せるか、時間を決めて実行<br/>
          ・ 第4象限（非重要・非緊急）: やらないか、最後に実行
        </Typography>
      </Box>
    </Box>
  );
}

export default MatrixView;