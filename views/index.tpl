<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">

%url = "/"

<html>
<head>
  <meta name="generator" content=
  "HTML Tidy for Linux (vers 7 December 2008), see www.w3.org">
  <link rel="stylesheet" type="text/css" href="/static/styles.css">

  <title>{{title}}</title>
</head>

<body>
  <div id="masthead">
%include header
  </div>
  <div id="page">
    <div id="middlecontainer">
%include sidebar
      <div id="main">
        <div id="squeeze">
%for entry in entries:
  %include entrydiv **entry
%end
        </div>
      </div>
    </div>

%include footer
  </div>
</body>
</html>
