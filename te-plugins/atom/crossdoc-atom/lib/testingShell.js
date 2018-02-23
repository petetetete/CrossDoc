
  console.log("I can run Node.js from within Atom!")

  const execFile = require('child_process').execFile;

  const child = execFile('cdoc', ['init'], (error, stdout, stderr) =>
          {
              if (error)
              {
                  console.error('stderr', stderr);
                  throw error;
              }
              console.log('stdout', stdout);
          });

  const child2 = execFile('cdoc', ['cc', '-text', 'testText', '-store', '1', '-set', '1'], (error, stdout, stderr) =>
          {
              if (error)
              {
                  console.error('stderr', stderr);
                  throw error;
              }
              console.log('stdout', stdout);
          });
  return "HELLO KRIS";
