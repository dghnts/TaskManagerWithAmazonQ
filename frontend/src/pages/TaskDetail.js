import React from 'react';
import { Typography, Box } from '@mui/material';

function TaskDetail() {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        タスク詳細
      </Typography>
      <Typography variant="body1">
        タスク詳細画面の実装予定
      </Typography>
    </Box>
  );
}

export default TaskDetail;