// load/LoadProvider.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Loading } from '../../../widgets/loading/ui/loading'; // Adjust the path as needed

interface LoadContextType {
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
}

const LoadContext = createContext<LoadContextType | undefined>(undefined);

export const LoadProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isLoading, setLoading] = useState(false);

  return (
    <LoadContext.Provider value={{ isLoading, setLoading }}>
      {isLoading && <Loading />}
      {children}
    </LoadContext.Provider>
  );
};

export const useLoad = () => {
  const context = useContext(LoadContext);
  if (!context) {
    throw new Error('useLoad must be used within a LoadProvider');
  }
  return context;
};
