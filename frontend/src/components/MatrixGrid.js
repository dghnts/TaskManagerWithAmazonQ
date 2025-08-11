import React from 'react';
import { 
  Grid, Paper, Typography, Box, Chip 
} from '@mui/material';

const quadrantTitles = {
  high_high: '第1象限: 重要かつ緊急',
  high_low: '第2象限: 重要だが緊急でない', 
  low_high: '第3象限: 重要でないが緊急',
  low_low: '第4象限: 重要でも緊急でもない'
};

const quadrantColors = {
  high_high: '#ffebee',
  high_low: '#fff3e0',
  low_high: '#e8f5e8', 
  low_low: '#f3e5f5'
};

function MatrixGrid({ matrixData }) {
  const renderQuadrant = (key, tasks, title) => (
    <Grid item xs={12} md={6} key={key}>
      <Paper 
        sx={{ 
          p: 2, 
          height: 300, 
          backgroundColor: quadrantColors[key],
          overflow: 'auto'
        }}
      >
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary" mb={2}>
          {tasks.length}件のタスク
        </Typography>
        
        <Box display="flex" flexDirection="column" gap={1}>
          {tasks.map(task => (
            <Paper 
              key={task.id} 
              sx={{ 
                p: 1.5, 
                cursor: 'pointer',
                '&:hover': { boxShadow: 2 }
              }}
              elevation={1}
            >
              <Typography variant="subtitle2" gutterBottom>
                {task.title}
              </Typography>
              <Box display="flex" gap={1}>
                <Chip 
                  label={task.status.replace('_', ' ')} 
                  size="small" 
                  variant="outlined"
                />
                {task.progress > 0 && (
                  <Chip 
                    label={`${task.progress}%`} 
                    size="small" 
                    color="primary"
                  />
                )}
              </Box>
            </Paper>
          ))}
          
          {tasks.length === 0 && (
            <Typography variant="body2" color="text.secondary" textAlign="center" mt={2}>
              タスクがありません
            </Typography>
          )}
        </Box>
      </Paper>
    </Grid>
  );

  // 実際のデータ構造に合わせて象限を組み立て
  const quadrant1 = matrixData.high_high || [];
  const quadrant2 = matrixData.high_low || [];
  const quadrant3 = matrixData.low_high || [];
  const quadrant4 = [...(matrixData.medium_low || []), ...(matrixData.low_medium || []), ...(matrixData.low_low || [])];

  return (
    <Grid container spacing={2}>
      {renderQuadrant('high_high', quadrant1, '第1象限: 重要かつ緊急')}
      {renderQuadrant('high_low', quadrant2, '第2象限: 重要だが緊急でない')}
      {renderQuadrant('low_high', quadrant3, '第3象限: 重要でないが緊急')}
      {renderQuadrant('low_low', quadrant4, '第4象限: 重要でも緊急でもない')}
    </Grid>
  );
}

export default MatrixGrid;