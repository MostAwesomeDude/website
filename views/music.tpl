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
<div id="body">
%include header

  <div id="main">
%for album, songs in albums.iteritems():
    <h2>{{"%s (%s)" % album}}</h2>
    <ul>
%for song in songs:
      <li>{{!'<a href="/%s">%s</a>' % song[0:2]}}</li>
%end
    </ul>
%end
  </div>

%include footer
</div>
</body>
</html>
