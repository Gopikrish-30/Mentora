import React from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import CourseStepper from '../src/components/CourseStepper';

const theme = createTheme({
  palette: {
    primary: {
      main: '#7C4DFF',
    },
    background: {
      default: '#F5F5F5',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          padding: '8px 24px',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <CourseStepper />
    </ThemeProvider>
  );
}

export default App;
