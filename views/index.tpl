%url = "/"

%include head title=title

<body>
<div id="body">
%include header

  <div id="main">
%for entry in entries:
  %include entrydiv **entry
%end
  </div>

%include footer preptime=time
</div>

%include valid

</body>
</html>
