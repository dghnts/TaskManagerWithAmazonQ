import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material';
import TaskList from './pages/TaskList';
import TaskDetail from './pages/TaskDetail';
import MatrixView from './pages/MatrixView';
import CalendarView from './pages/CalendarView';
import Navigation from './components/Navigation';

function App() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            タスク管理アプリ
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Navigation />
      
      <Container maxWidth="xl" sx={{ mt: 2 }}>
        <Routes>
          <Route path="/" element={<TaskList />} />
          <Route path="/tasks" element={<TaskList />} />
          <Route path="/tasks/:id" element={<TaskDetail />} />
          <Route path="/matrix" element={<MatrixView />} />
          <Route path="/calendar" element={<CalendarView />} />
        </Routes>
      </Container>
    </Box>
  );
}

export default App;