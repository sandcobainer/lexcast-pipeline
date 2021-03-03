var fs = require('fs');
var readline = require('readline');
var {google} = require('googleapis');
var OAuth2 = google.auth.OAuth2;

// If modifying these scopes, delete your previously saved credentials
// at ~/.credentials/youtube-nodejs-quickstart.json
var SCOPES = ['https://www.googleapis.com/auth/youtube.readonly'];
var TOKEN_DIR = (process.env.HOME || process.env.HOMEPATH ||
    process.env.USERPROFILE) + '/.credentials/';
var TOKEN_PATH = TOKEN_DIR + 'youtube-nodejs-quickstart.json';

// Load client secrets from a local file.
fs.readFile('client_secret.json', function processClientSecrets(err, content) {
  if (err) {
    console.log('Error loading client secret file: ' + err);
    return;
  }
  // Authorize a client with the loaded credentials, then call the YouTube API.
  authorize(JSON.parse(content), getPlaylistItems);
});

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 *
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
function authorize(credentials, callback) {
  var clientSecret = credentials.installed.client_secret;
  var clientId = credentials.installed.client_id;
  var redirectUrl = credentials.installed.redirect_uris[0];
  var oauth2Client = new OAuth2(clientId, clientSecret, redirectUrl);

  // Check if we have previously stored a token.
  fs.readFile(TOKEN_PATH, function(err, token) {
    if (err) {
      getNewToken(oauth2Client, callback);
    } else {
      oauth2Client.credentials = JSON.parse(token);
      callback(oauth2Client);
    }
  });
}

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 *
 * @param {google.auth.OAuth2} oauth2Client The OAuth2 client to get token for.
 * @param {getEventsCallback} callback The callback to call with the authorized
 *     client.
 */
function getNewToken(oauth2Client, callback) {
  var authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES
  });
  console.log('Authorize this app by visiting this url: ', authUrl);
  var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  rl.question('Enter the code from that page here: ', function(code) {
    rl.close();
    oauth2Client.getToken(code, function(err, token) {
      if (err) {
        console.log('Error while trying to retrieve access token', err);
        return;
      }
      oauth2Client.credentials = token;
      storeToken(token);
      callback(oauth2Client);
    });
  });
}

/**
 * Store token to disk be used in later program executions.
 *
 * @param {Object} token The token to store to disk.
 */
function storeToken(token) {
  try {
    fs.mkdirSync(TOKEN_DIR);
  } catch (err) {
    if (err.code != 'EEXIST') {
      throw err;
    }
  }
  fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
    if (err) throw err;
    console.log('Token stored to ' + TOKEN_PATH);
  });
}

/**
 * Lists the names and IDs of up to 10 files.
 *
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 */
function getChannel(auth) {
  var service = google.youtube('v3');
  service.channels.list({
    auth: auth,
    part: 'snippet,contentDetails,statistics',
    forUsername: 'lexfridman'
  }, function(err, response) {
    if (err) {
      console.log('The API returned an error: ' + err);
      return;
    }
    var channels = response.data.items;
    if (channels.length == 0) {
      console.log('No channel found.');
    } else {
      console.log('This channel\'s ID is %s. Its title is \'%s\', and ' +
                  'it has %s views.',
                  channels[0].id,
                  channels[0].snippet.title,
                  channels[0].statistics.viewCount);
    }
  });
}

function getChannelUrls(auth) {
  var service = google.youtube('v3');
  service.subscriptions.list({
    auth: auth, part: 'snippet,contentDetails', 
    mine:true, maxResults:50}, 
    function(err, response) {
        if(!err) {
            var items =  response.data.items
            for ( i in items) {
              console.log(items[i].snippet.title, items[i].snippet.channelId)
            }
        }
    }
  );
}

function getPlaylistId(auth) {
  var service = google.youtube('v3');
  service.channels.list({ auth: auth, part: 'contentDetails', 
            id:'UCySJqHS5WFTuVePIQBEI94A', maxResults:50 }, 
            function(err, response) {
                var items =  response.data.items
                
                var channelPlaylistId = items[0].contentDetails.relatedPlaylists.uploads;
                console.log(items);
            }
        );
}

function getPlaylistItems(auth) {
  var service = google.youtube('v3'), output = {};
  service.playlistItems.list({    auth: auth, part: 'snippet', 
        playlistId:'PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4',
        pageToken:'CGQQAA',
        maxResults:150}, 
        function(err, response) {
            var items = response.data.items
            for (i in items) {
              output[items[i].snippet.position] =  { 
                'title':items[i].snippet.title,
                'publishedAt': items[i].snippet.publishedAt,
                'description': items[i].snippet.description,
                'videoId': items[i].snippet.resourceId.videoId
              }
            }
            console.log(output)
            console.log(response.data.nextPageToken)
            
            fs.writeFile("./urls3.json", JSON.stringify(output), (err) => {
              if (err) {
                  console.error(err);
                  return;
              };
              console.log("File has been created");
          });
        }

    );
}