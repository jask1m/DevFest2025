import { useState } from 'react';

function Landing({ setUseCase }: { setUseCase: (value: string) => void }) {
  const [inputValue, setInputValue] = useState('');

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
    setUseCase(event.target.value);
  };

  return (
    <>
      <h1 className="bg-green-200">landing</h1>
      <div>
        <input
          type="text"
          value={inputValue}
          onChange={handleChange}
          placeholder="Enter use case"
        />
      </div>
    </>
  );
}

export default Landing;