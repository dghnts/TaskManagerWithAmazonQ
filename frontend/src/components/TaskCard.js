import React from 'react';
import { 
  Card, CardContent, CardActions, Typography, Chip, 
  LinearProgress, IconButton, Box 
} from '@mui/material';
import { Edit, Delete, Comment, Assignment } from '@mui/icons-material';

const priorityColors = {
  high: 'error',
  medium: 'warning', 
  low: 'success'
};

const urgencyColors = {
  high: 'error',
  medium: 'warning',
  low: 'info'
};

const statusColors = {
  not_started: 'default',
  in_progress: 'primary',
  completed: 'success',
  on_hold: 'warning'
};

function TaskCard({ task, onEdit, onDelete, onClick }) {
  const handleCardClick = (e) => {
    if (e.target.closest('button')) return;
    onClick?.(task.id);
  };

  return (
    <Card 
      sx={{ 
        mb: 2, 
        cursor: 'pointer',
        '&:hover': { boxShadow: 3 }
      }}
      onClick={handleCardClick}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
          <Typography variant="h6" component="h3" sx={{ flexGrow: 1 }}>
            {task.title}
          </Typography>
          <Chip 
            label={task.status.replace('_', ' ')} 
            color={statusColors[task.status]}
            size="small"
          />
        </Box>
        
        {task.description && (
          <Typography variant="body2" color="text.secondary" mb={2}>
            {task.description.length > 100 
              ? `${task.description.substring(0, 100)}...` 
              : task.description
            }
          </Typography>
        )}

        <Box display="flex" gap={1} mb={2}>
          <Chip 
            label={`優先度: ${task.priority}`} 
            color={priorityColors[task.priority]}
            size="small"
          />
          <Chip 
            label={`緊急度: ${task.urgency}`} 
            color={urgencyColors[task.urgency]}
            size="small"
          />
          <Chip 
            label={task.category} 
            variant="outlined"
            size="small"
          />
        </Box>

        {task.progress > 0 && (
          <Box mb={2}>
            <Typography variant="body2" color="text.secondary" mb={1}>
              進捗: {task.progress}%
            </Typography>
            <LinearProgress variant="determinate" value={task.progress} />
          </Box>
        )}

        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" gap={2}>
            {task.subtask_count > 0 && (
              <Box display="flex" alignItems="center" gap={0.5}>
                <Assignment fontSize="small" color="action" />
                <Typography variant="caption">
                  {task.completed_subtasks}/{task.subtask_count}
                </Typography>
              </Box>
            )}
            {task.comment_count > 0 && (
              <Box display="flex" alignItems="center" gap={0.5}>
                <Comment fontSize="small" color="action" />
                <Typography variant="caption">{task.comment_count}</Typography>
              </Box>
            )}
          </Box>
          
          {task.due_date && (
            <Typography variant="caption" color="text.secondary">
              期限: {new Date(task.due_date).toLocaleDateString('ja-JP')}
            </Typography>
          )}
        </Box>
      </CardContent>
      
      <CardActions>
        <IconButton size="small" onClick={() => onEdit?.(task)}>
          <Edit />
        </IconButton>
        <IconButton size="small" onClick={() => onDelete?.(task.id)}>
          <Delete />
        </IconButton>
      </CardActions>
    </Card>
  );
}

export default TaskCard;