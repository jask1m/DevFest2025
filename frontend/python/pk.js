const util = require("util");
const path = require("path");
const child_process = require("child_process");

const pythonScriptPath = path.resolve("logger.py");
const pythonExecutablePath = path.resolve("venv/bin/python3");
const exec = util.promisify(child_process.exec);

async function runWithPrivileges() {
  console.log(`Requesting privileges via pkexec...`);

  const python = child_process.spawn("pkexec", [pythonExecutablePath, pythonScriptPath], {
    stdio: "inherit",
  });

  python.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);
  });

  python.on("error", (err) => {
    console.error(`Failed to start process: ${err}`);
  });
}

runWithPrivileges();
