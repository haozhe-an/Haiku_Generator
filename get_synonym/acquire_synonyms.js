var unirest = require('unirest');
const http = require('http');

function get_synonym(first_line){
  for (var i = 0; i<first_line.length; i++){
    unirest.get(`https://wordsapiv1.p.mashape.com/words/${first_line[i]}`)
    .header("X-Mashape-Key", "G1FZHetoxLmshayLcZLwlNuBRD4rp1QEBpRjsnf24FQwhS9Th0")
    .header("Accept", "application/json")
    .end(function (result) {
      for (var c in result.body.results) {
        if(result.body.results[c].hasOwnProperty('similarTo')){
          for (var i in result.body.results[c].similarTo) {
            console.log(result.body.results[c].similarTo[i]);
          }
        }
        if(result.body.results[c].hasOwnProperty('synonyms')){
          for (var i in result.body.results[c].synonyms){
            console.log(result.body.results[c].synonyms[i]);
          }
        }
        if(result.body.results[c].hasOwnProperty('also')){
          for (var i in result.body.results[c].also){
            console.log(result.body.results[c].also[i]);
          }
        }
      }
    });
  }
}
//check if there is no input
if (process.argv.length == 2){
  console.log("error");
  return;
}
var first_line = [];
for (var i = 2; i<process.argv.length; i++){
  first_line.push(process.argv[i]);
}
get_synonym(first_line);
