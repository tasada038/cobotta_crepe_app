const path = require("path");

const spawn = require("child_process").spawn,
  ls = spawn(
    "pyinstaller",
    [
      "-w",
      "--onefile",
      `--add-data web_app/templates${path.delimiter}templates`,
      `--add-data web_app/static${path.delimiter}static`,
      `--add-data web_app/robot${path.delimiter}robot`,
      `--add-data web_app/pybcapclient${path.delimiter}pybcapclient`,
      `--add-data web_app/models${path.delimiter}models`,
      "--distpath dist-python",
      "server.py",
      "web_app/__init__.py",
      "web_app/config.py",
      "web_app/views.py",
      "web_app/customer_info.db",
    ],
    {
      shell: true,
    }
  );

ls.stdout.on("data", function (data) {
  // stream output of build process
  console.log(data.toString());
});

ls.stderr.on("data", function (data) {
  console.log("Packaging error: " + data.toString());
});
ls.on("exit", function (code) {
  console.log("child process exited with code " + code.toString());
});