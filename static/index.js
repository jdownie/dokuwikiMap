var wikiApp = new Vue(
{ el: '#WikiMap',
  delimiters: ['[[',']]'],
  data: function() {
    return {
      node: '/',
      menu: null,
      wiki: null
    };
  },
  mounted: function() {
    jQuery.get( '/wiki.json'
              , {}
              , function(data) {
                  wikiApp.wiki = data;
                }
              );
    jQuery.get( '/menu.json'
              , {}
              , function(data) {
                  wikiApp.menu = data;
                }
              );
  },
  filters: {
    inboundCount: function(node) {
      var ret = 0;
      for (k in this.wikiApp.wiki) {
        var dsts = wikiApp.wiki[k];
        if (dsts != undefined) {
          ret += ( dsts.indexOf(node) == -1 ? 0 : 1 );
        }
      }
      return ret;
    },
    outboundCount: function(node) {
      return wikiApp.wiki[node].length;
    }
  },
  methods: {
    openWiki: function(node) {
      window.open('https://wiki.hsbne.org' + node, node);
    }
  }
});
