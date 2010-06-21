<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">

%import bottle

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
    <div id="header" class="clear-block">
      <div class="header-right">
        <div class="header-left">

          <div id="logo-title">
%if bottle.request.fullpath != url:
<a href={{url}} title="Home"><img src= "/static/matrix-keys.png" alt="Home"
id="logo" name="logo" /></a>
%else:
<img src= "/static/matrix-keys.png" alt="Home" id="logo" name="logo" />
%end
          </div><!-- /logo-title -->

          <div id="name-and-slogan">
%if bottle.request.fullpath != url:
<h1 id='site-name'><a href={{url}} title="Home">Corbin Simpson</a></h1>
%else:
<h1 id='site-name'>Corbin Simpson</h1>
%end
            <div id='site-slogan'>
              Most awesome, dude!
            </div>
          </div><!-- /name-and-slogan -->
        </div><!-- /header-left -->
      </div><!-- /header-right -->
    </div><!-- /header -->
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
