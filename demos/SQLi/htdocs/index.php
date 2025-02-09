<?php
  $browser_language = (string) (isset($_SERVER['HTTP_ACCEPT_LANGUAGE']) === true && $_SERVER['HTTP_ACCEPT_LANGUAGE'] !== '') ? strtok(strip_tags($_SERVER['HTTP_ACCEPT_LANGUAGE']), ',') : '';
  $browser_language = (isset($_GET['language']) === true && $_GET['language'] !== '') ? $_GET['language'] : $browser_language;
  $language = (string) '';
  switch (substr($browser_language, 0, 2)) {
    case 'de':
      $language = 'de';
      break;
    case 'en':
      $language = 'en';
      break;
    default:
      $language = 'en';
  }

  $available_languages = (array) [
    (array) [
        'name' => (string) 'English',
        'token' => (string) 'en',
    ],
    (array) [
        'name' => (string) 'Deutsch',
        'token' => (string) 'de',
    ],
  ];
    
  $switch_language = (string) '';
  foreach ($available_languages as $available_language) {
    if ($available_language['token'] !== $language) {
        $switch_language .= '<a href="'.strip_tags($_SERVER['PHP_SELF']).'?language='.$available_language['token'].'" lang="'.$available_language['token'].'" hreflang="'.$available_language['token'].'">'.$available_language['name'].'</a> | ';
    }
  }
  $switch_language = substr($switch_language, 0, -3);
?>

<!DOCTYPE html>
<html lang="<?php echo $language; ?>">
  <head>
    <meta charset="UTF-8">
    <title>MAMP</title>
	<link rel="icon" href="data:image/svg+xml,%3Csvg%20width%3D%22100%25%22%20height%3D%22100%25%22%20viewBox%3D%220%200%202048%202048%22%20version%3D%221.1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20xml%3Aspace%3D%22preserve%22%20style%3D%22fill-rule%3Aevenodd%3Bclip-rule%3Aevenodd%3Bstroke-linejoin%3Around%3Bstroke-miterlimit%3A1.41421%3B%22%3E%3Ccircle%20cx%3D%221035.06%22%20cy%3D%221039.06%22%20r%3D%22814.588%22%20style%3D%22fill%3Argb%2897%2C97%2C97%29%3B%22%2F%3E%3Cg%20transform%3D%22matrix%281%2C0%2C0%2C1%2C915.735%2C630.118%29%22%3E%3Ctext%20x%3D%220px%22%20y%3D%220px%22%20style%3D%22font-family%3A%5C%27ArialMT%5C%27%2C%20%5C%27Arial%5C%27%2C%20sans-serif%3Bfont-size%3A12px%3Bfill%3Argb%2837%2C124%2C175%29%3B%22%3E257CAF%3C%2Ftext%3E%3C%2Fg%3E%3Cg%20transform%3D%22matrix%2839.9757%2C0%2C0%2C39.9757%2C435.174%2C509.385%29%22%3E%3Cpath%20d%3D%22M0.63%2C10.25C0.94%2C8.105%203.335%2C1.421%2010.06%2C0.153C14.028%2C-0.595%2018.922%2C1.462%2022.358%2C4.946C20.645%2C6.122%2019.499%2C7.138%2018.634%2C8.372C19.279%2C10.767%2021.185%2C11.742%2022.528%2C12.147C21.041%2C11.249%2020.102%2C10.4%2019.521%2C8.591C22.701%2C4.81%2026.106%2C3.587%2026.394%2C3.558C29.053%2C5.679%2030.93%2C9.548%2030.863%2C13.622C30.784%2C18.339%2028.219%2C23.2%2025.278%2C25.162C24.874%2C25.355%2023.945%2C24.846%2023.818%2C24.294C24.42%2C22.896%2025.844%2C19.491%2026.019%2C16.948C26.185%2C14.507%2024.569%2C13.074%2023.213%2C14.838C21.328%2C17.993%2020.506%2C21.913%2019.683%2C26.142C18.298%2C26.538%2015.948%2C26.638%2014.932%2C26.096C14.803%2C23.479%2015.413%2C19.009%2013.677%2C17.442C12.933%2C16.769%2012.199%2C17.081%2011.701%2C17.701C10.446%2C19.255%2010.471%2C23.286%2010.714%2C25.899C9.31%2C26.766%206.931%2C26.585%205.427%2C26.047C4.824%2C21.94%203.407%2C16.935%202.248%2C13.103C1.925%2C14.643%201.769%2C16.474%201.819%2C18.048C1.045%2C17.418%200.164%2C14.105%200.63%2C10.25Z%22%20style%3D%22fill%3Awhite%3B%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E" type="image/svg+xml">
    <style>
      body {
        font-family: Arial, Helvetica, sans-serif;
        font-size: .9em;
        color: #000000;
        background-color: #FFFFFF;
        margin: 0;
        padding: 10px 20px 20px 20px;

        background-image: url('data:image/svg+xml;utf8,<svg width="100%" height="100%" viewBox="0 0 2048 2048" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;"><circle cx="1035.06" cy="1039.06" r="814.588" style="fill:rgb(97,97,97);"/><g transform="matrix(1,0,0,1,915.735,630.118)"><text x="0px" y="0px" style="font-family:\'ArialMT\', \'Arial\', sans-serif;font-size:12px;fill:rgb(37,124,175);">257CAF</text></g><g transform="matrix(39.9757,0,0,39.9757,435.174,509.385)"><path d="M0.63,10.25C0.94,8.105 3.335,1.421 10.06,0.153C14.028,-0.595 18.922,1.462 22.358,4.946C20.645,6.122 19.499,7.138 18.634,8.372C19.279,10.767 21.185,11.742 22.528,12.147C21.041,11.249 20.102,10.4 19.521,8.591C22.701,4.81 26.106,3.587 26.394,3.558C29.053,5.679 30.93,9.548 30.863,13.622C30.784,18.339 28.219,23.2 25.278,25.162C24.874,25.355 23.945,24.846 23.818,24.294C24.42,22.896 25.844,19.491 26.019,16.948C26.185,14.507 24.569,13.074 23.213,14.838C21.328,17.993 20.506,21.913 19.683,26.142C18.298,26.538 15.948,26.638 14.932,26.096C14.803,23.479 15.413,19.009 13.677,17.442C12.933,16.769 12.199,17.081 11.701,17.701C10.446,19.255 10.471,23.286 10.714,25.899C9.31,26.766 6.931,26.585 5.427,26.047C4.824,21.94 3.407,16.935 2.248,13.103C1.925,14.643 1.769,16.474 1.819,18.048C1.045,17.418 0.164,14.105 0.63,10.25Z" style="fill:white;"/></g></svg>');
        background-repeat: no-repeat;
        background-size: 80px 80px;
        background-position: 17px 5px;
      }

      samp {
        font-size: 1.3em;
      }

      a {
        color: #000000;
        background-color: #FFFFFF;
      }

      sup a {
        text-decoration: none;
      }

      hr {
        margin-left: 90px;
        height: 1px;
        color: #000000;
        background-color: #000000;
        border: none;
      }

      .text {
        width: 80%;
        margin-left: 90px;
        line-height: 140%;
      }
    </style>
  </head>
  <body>
    <?php if ($language === 'de'): ?>
      <p class="text"><strong>Willkommen bei MAMP</strong></p>
      <p class="text">Wenn Sie diese Seite sehen, dann bedeutet dies, dass MAMP erfolgreich eingerichtet und gestartet wurde. Sie können jetzt Ihren <span lang="en">Web</span>-Inhalt hinzufügen, diese Platzhalter-Seite<sup><a href="#footnote-1">1</a></sup> sollten Sie ersetzen <abbr title="beziehungsweise">bzw.</abbr> löschen.</p>
      <p class="text">
        <span lang="en">Server-Software</span>: <samp><?php echo strip_tags(htmlentities($_SERVER['SERVER_SOFTWARE'], ENT_QUOTES, 'UTF-8')); ?></samp><br>
        <span lang="en">Server-Name</span>: <samp><?php echo strip_tags(htmlentities($_SERVER['SERVER_NAME'], ENT_QUOTES, 'UTF-8')); ?></samp><br>
        <span lang="en">Document-Root</span>: <samp><?php echo strip_tags(htmlentities($_SERVER['DOCUMENT_ROOT'], ENT_QUOTES, 'UTF-8')); ?></samp><br>
        Protokoll: <samp><?php echo ((isset($_SERVER['HTTPS']) === true && $_SERVER['HTTPS'] !== 'off') ? '<abbr lang="en" title="Hypertext Transfer Protocol Secure">https</abbr>' : '<abbr lang="en" title="Hypertext Transfer Protocol">http</abbr>'); ?></samp><br>
        <abbr lang="en" title="Hypertext Preprocessor">PHP</abbr> <samp><?php echo phpversion(); ?></samp>
      </p>
      <p class="text" id="footnote-1"><small><sup>1</sup> Datei: <samp>index.php</samp></small></p>
      <hr>
      <p class="text">This page in: <?php echo $switch_language; ?></p>
    <?php elseif ($language == 'en'): ?>
      <p class="text"><strong>Welcome to MAMP</strong></p>
      <p class="text">If you can see this page, MAMP has been properly configured &amp; launched and is now all set to serve your web content. This placeholder page<sup><a href="#footnote-1">1</a></sup> should be replaced or deleted.</p>
      <p class="text">
        Server software: <samp><?php echo strip_tags(htmlentities($_SERVER['SERVER_SOFTWARE'], ENT_QUOTES, 'UTF-8')); ?></samp>  <br>
        Server name: <samp><?php echo strip_tags(htmlentities($_SERVER['SERVER_NAME'], ENT_QUOTES, 'UTF-8')); ?></samp>  <br>
        Document root: <samp><?php echo strip_tags(htmlentities($_SERVER['DOCUMENT_ROOT'], ENT_QUOTES, 'UTF-8')); ?></samp>  <br>
        Protocol: <samp><?php echo ((isset($_SERVER['HTTPS']) === true && $_SERVER['HTTPS'] !== 'off') ? '<abbr title="Hypertext Transfer Protocol Secure">https</abbr>' : '<abbr title="Hypertext Transfer Protocol">http</abbr>'); ?></samp><br>
        <abbr title="Hypertext Preprocessor">PHP</abbr>: <samp><?php echo phpversion(); ?></samp>
      </p>
      <p class="text" id="footnote-1"><small><sup>1</sup> File: <samp>index.php</samp></small></p>
      <hr>
      <p class="text">Diese Seite auf: <?php echo $switch_language; ?></p>
    <?php endif; ?>
  </body>
</html>