import React from 'react';
import { Typography, Box } from '@mui/material';

function TaskList() {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        タスク一覧
      </Typography>
      <Typography variant="body1">
        タスク一覧画面の実装予定
      </Typography>
    </Box>
  );
}

export default TaskList;