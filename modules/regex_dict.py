''' regex_dict.py'''

regex_dict = {
    '<h3>FLIGHT CHARACTERISTICS</h3>.+?</a></p>':
    '',
    '<p>Information about <a title="Information about this plastic type.+?</p>':
    '',
    '<h3>More Information</h3> <p>.+':
    '',
    '<h3>SPECIFICATIONS</h3>.+?<li>Best':
    '<h3>SPECIFICATIONS</h3> <ul> <li>Best',
    'Check out how it flies here.</p> <p><!-- mceItemMediaService.+?mceItemMediaService --></p>':
    ''
}
