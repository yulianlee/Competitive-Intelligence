
 // Require libraries
const express = require('express')
var path = require('path');
var fs = require('fs');
let {PythonShell} = require('python-shell')
var port = process.env.PORT || 8080;

// Define app
const app = express();

let wd = path.join(__dirname, '/temp')
fs.readdir(wd, (err, files) => {
  if (err) throw err;

  const number = files.length
  for (const file of files) {
    fs.unlink(path.join(wd, file), err => {
      if (err) throw err;
    });
  }

  console.log(number+' Files deleted from ' + path.join(__dirname, '/temp') )
});

let wd2 = path.join(__dirname, '/pygal')
fs.readdir(wd2, (err, files2) => {
  if (err) throw err;

  const number2 = files2.length
  for (const file2 of files2) {
    fs.unlink(path.join(wd2, file2), err => {
      if (err) throw err;
    });
  }

  console.log(number2+' Files deleted from ' + path.join(__dirname, '/pygal') )
});


app.get("/titles", function (req, res) {
  console.log("running on /titles!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('title.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log(request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO title.py!!")
  console.log("NOW LOADING FOR TITLES!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})

});

app.get("/proj_details", function (req, res) {
  console.log("running on /proj_details!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('project_details.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log(request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO project_details.py!!")
  console.log("NOW LOADING FOR PROJECT DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})

});

app.get("/biddiff", function(req,res){
  console.log("running on /biddiff!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('company_plots_final.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO company_plot_final.py!!")
  console.log("NOW LOADING FOR COMPANY PLOT DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});



app.get("/bidindex", function(req,res){
  console.log("running on /bidindex!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('Bid_Index.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO Bid_Index.py!!")
  console.log("NOW LOADING FOR COMPANY PLOT DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');


        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/dbsearch", function(req,res){
  console.log("running on /dbsearch!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('dbsearch.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log(request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO dbsearch.py!!")
  console.log("NOW LOADING FOR DATABASE SEARCH DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/company_details", function(req,res){
  console.log("running on /company_details!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('companydetails.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO companydetails.py!!")
  console.log("NOW LOADING FOR COMPANY DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');


        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});


app.get("/biddiff", function(req,res){
  console.log("running on /biddiff!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('company_plots.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO company_search.py!!")
  console.log("NOW LOADING FOR COMPANY PLOT DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});
app.get("/agency_details", function(req,res){
  console.log("running on /agency_details!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('agency_details.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO agency_details.py!!")
  console.log("NOW LOADING FOR AGENCY DETAILS!! :)")

  console.log("request is" +request)
  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/agency_plot", function(req,res){
  console.log("running on /agency_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('agency_plots.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO agency_plots.py!!")
  console.log("NOW LOADING FOR AGENCY PLOT DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/bulk_details", function(req,res){
  console.log("running on /bulk_details!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('bulk_tenders.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log(request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO bulk_tenders.py!!")
  console.log("NOW LOADING FOR BULK TENDER SEARCH DETAILS!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/intro_page", function(req,res){
  console.log("running on /intro_page!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('top_3_by_value.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log("request is" +request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO top_3_by_value.py!!")
  console.log("NOW LOADING FOR INTRO PAGE!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/intro_plot", function(req,res){
  console.log("running on /intro_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('intro_plot.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log("request is" +request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO intro_plot.py!!")
  console.log("NOW LOADING FOR INTRO PLOT!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/agency_pie_plot", function(req,res){
  console.log("running on /agency_pie_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('agency_pie_plot.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log("request is" +request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO agency_pie_plot.py!!")
  console.log("NOW LOADING FOR AGENCY PIE PLOT!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});



app.get("/agency_bar_plot", function(req,res){
  console.log("running on /agency_bar_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('barplot.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log("request is" +request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO bar_time.py!!")
  console.log("NOW LOADING FOR AGENCY BAR PLOT!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

app.get("/agency_line_plot", function(req,res){
  console.log("running on /agency_line_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('line_plot.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log("request is" +request)

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO line_plot.py!!")
  console.log("NOW LOADING FOR AGENCY LINE PLOT!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});





app.get("/company_whisker_plot", function(req,res){
  console.log("running on /company_whisker_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('company_box_whisker.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO company_box_whisker.py!!")
  console.log("NOW LOADING FOR COMPANY BOX WHISKER PLOT!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        // console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        // console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});


app.get("/company_bar_plot", function(req,res){
  console.log("running on /company_bar_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('company_bar.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO company_bar.py!!")
  console.log("NOW LOADING FOR COMPANY BAR PLOT!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        // console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        // console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});


app.get("/set_category", function(req,res){
  console.log("running on /set_category!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('agency_return_proc_cat.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD

  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO agency_return_proc_cat.py!!")
  console.log("NOW LOADING FOR PROCUREMENT CATEGORY!! :)")


  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        // console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        // console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});


app.get("/gauge_plot", function(req,res){
  console.log("running on /gauge_plot!")

  var params = JSON.stringify(req.query); // req.query is the input
  var fpath = path.join(__dirname, '/pyfile'); // set path for the python file

  PythonShell.defaultOptions = { scriptPath: fpath };  // set path to the pythonShell
  let pyshell = new PythonShell('agency_gauge_plot.py'); // Create a new pythonShell to run main.py

  // Define request
  request = JSON.stringify(params)

  // console log request to CMD
  console.log(params)
  // sending request to python
  pyshell.send(request, { mode: 'text'})
  console.log("SENDING A REQUEST TO agency_gauge.py!!")



  // define what to do after receive a response from python
  pyshell.on('message',function (message,err) {
  		// if got any error, console log 'error' on cmd and show error on index.html
        if (err){
          console.log("error")
          res.send(err);
        }

        // message = output
        console.log("fetched")
        // console.log(message)

        // set header and send message to html
        res.set('Content-Type', 'text/plain')

        let contents = fs.readFileSync(message, 'utf8');
        // console.log(contents);

        res.send(contents)
        // end session
        res.end()

      });

  //end pythonShell
  pyshell.end(function (err,code,signal) {
      console.log("pyend")
    if (err){console.log(err)}})
});

// app.get("/",function(req,res){
//   res.send(express.static(__dirname + '/'))
// })

// Load Html
app.use('/', express.static(__dirname + '/'));

// use 3000 port to listen
// app.listen(process.env.POrt||3000, () => {
//   console.log('Example app listening on port 3000!')
// });
app.listen(port)
