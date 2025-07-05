import React from 'react';

const LoadingScreen = () => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-75">
      <div className="relative w-60 h-60">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="w-60 h-60 bg-[url("data:image/svg+xml,%3Csvg width=\'60\\' height=\'60\\' viewBox=\'0 0 60 60\\' fill=\'none\\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Ccircle cx=\'30\\' cy=\'30\\' r=\'30\\' fill=\'%23333333\\' fill-opacity=\'0.1\\'/%3E%3Ccircle cx=\'30\\' cy=\'30\\' r=\'30\\' fill=\'%23ffffff\\' fill-opacity=\'0.1\\'/%3E%3Ccircle cx=\'30\\' cy=\'30\\' r=\'30\\' fill=\'%23333333\\' fill-opacity=\'0.1\\'/%3E%3Ccircle cx=\'30\\' cy=\'30\\' r=\'30\\' fill=\'%23ffffff\\' fill-opacity=\'0.1\\'/%3E%3C/svg%3E" )] bg-cover bg-center">
          </div>
        </div>

        {/* Spinner */}
        <div className="absolute inset-0 flex items-center justify-center">
          <svg className="animate-spin h-16 w-16 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>
    </div>
   );
};

export default LoadingScreen;
