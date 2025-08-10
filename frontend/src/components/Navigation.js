import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Tabs, Tab, Box } from '@mui/material';
import { List, GridView, CalendarMonth } from '@mui/icons-material';

function Navigation() {
  const navigate = useNavigate();
  const location = useLocation();

  const getTabValue = () => {
    if (location.pathname.startsWith('/matrix')) return 1;
    if (location.pathname.startsWith('/calendar')) return 2;
    return 0; // デフォルトは一覧
  };

  const handleChange = (event, newValue) => {
    switch (newValue) {
      case 0:
        navigate('/tasks');
        break;
      case 1:
        navigate('/matrix');
        break;
      case 2:
        navigate('/calendar');
        break;
      default:
        navigate('/tasks');
    }
  };

  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
      <Tabs value={getTabValue()} onChange={handleChange}>
        <Tab icon={<List />} label="一覧" />
        <Tab icon={<GridView />} label="マトリックス" />
        <Tab icon={<CalendarMonth />} label="カレンダー" />
      </Tabs>
    </Box>
  );
}

export default Navigation;