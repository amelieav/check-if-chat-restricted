// runImageRecognition.js
const { exec } = require('child_process');

const pythonScript = 'imageRecognition.py'; // Replace this with your Python file name

exec(`python ${pythonScript}`, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error executing the Python script: ${error.message}`);
    return;
  }

  console.log(`Python script output: ${stdout}`);
  if (stderr) {
    console.error(`Python script error: ${stderr}`);
  }
});