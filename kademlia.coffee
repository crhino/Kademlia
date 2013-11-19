$ ->
  k = 5
  width = 960
  height = 500
  bits = 8

  node_id = 0

  color = d3.scale.category20()

  force = d3.layout.force().size([width, height])

  svg = d3.select("body").append("svg").attr("width", width).attr("height", height)


  # Node model, implements much of the Kademlia interface
  class Node extends Backbone.Model
    initialize: (node) ->
      this.set("buckets", ([] for num in [0..bits-1]))
      @set("id", node_id)
      if (node != null)
        @add_node(node)
        node.find_node(this, @id
                  , (nodes) =>
                      console.log("node " + node_id)
                      console.log(nodes)
                      @add_node(n) for n in nodes)

      node_id++


    pick_bucket: (key) ->

    # Takes in a key and returns the XOR metric of the key and this.id
    xor: (key) ->
      return @get("id") ^ key


    find_bucket: (key) ->
      dist = @xor(key)
      i = 0
      i++ until ((dist >> i) == 0)
      return i

    # Adds a node to the appropriate bucket.
    add_node: (node) ->
      id = node.get("id")
      if(id == @id)
        return null
      temp = false
      i = @find_bucket(id)
      buckets = @get("buckets")
      console.log("ADD node: " + id + " to node: " + @id)
      console.log(node)
      console.log(buckets[i])
      for n in buckets[i]
        do (n) ->
          if(id is n.get("id"))
            temp = true
      if(temp)
        return null
      console.log("after")
      buckets[i].push(node)
 

    ping_node: (id, callback) ->
      buckets = this.get("buckets")
      console.log("Node buckets: " + buckets)
      #callback(

    store_value: (source, key, val) ->


    find_node: (source, id, callback) ->
      @add_node(source)
      callback(@get("buckets")[@find_bucket(id)])

    find_value: (source, key, callback) ->

    # Creates a link object for d3.
    linkify: (node) ->
      return {"source": this
              ,"target": node
              ,"distance": @xor(node.get("id"))}

    # Foldl over the buckets array to get a specific node's links.
    get_links: =>
      links = _.foldl(@get("buckets")
                      , (init, nodes) =>
                          init.push(@linkify(node)) for node in nodes
                          #console.log("Get node links for: " + @id)
                          #console.log(init)
                          return init
                      , [])
      return links


  class Network extends Backbone.Collection
    model: Node

    get_links: ->
      return _.foldl(@models
                     , (init, model) ->
                          return init.concat(model.get_links())
                     , [])
      
    test: ->
      @models[4].add_node(@models[3])
      @models[4].add_node(@models[6])
      @models[4].add_node(@models[8])
      @models[7].add_node(@models[9])
      @models[9].add_node(@models[2])
      @models[11].add_node(@models[6])
      @models[12].add_node(@models[6])

  class NetworkView extends Backbone.View
    el: '.network-view'
    initialize: ->
      console.log('init')
      this.listenTo(this.collection, {
        add: this.addNode
      })
      this.render()

    render: ->
      this.$el.html("<h1>Kademlia Network Simulation</h1>")
      #svg.append("circle").attr("class", "node")
      #.attr("r", 20)
      #.attr("cx", 100).attr("cy", 100)
      links = @collection.get_links()
      nodes = @collection.models

      console.log(links)

      force
      .nodes(nodes)
      .links(links)
      .charge(-800)
      .linkDistance( (link, i) -> return link.distance*10)
      .start()

      link = svg.selectAll(".link")
             .data(links).enter().append("line")
             .attr("class", "link")
             .style("stroke-width", 3)

      console.log(link)
             #.attr("d"
             #       , (d) -> 
             #           console.log(d)
             #           d.tension(d.distance/256))
     
      node = svg.selectAll(".node")
             .data(nodes).enter().append("circle")
             .attr("class", "node")
             .attr("r", 9)
             .style("fill", color(3))
             .style("stroke-width", 2)

      node.append("title").text( (d) -> return  "Node " + d.id)
      
      console.log(node)
      force.on("tick"
               , -> 
                  link.attr("x1", (d) -> return d.source.x)
                      .attr("y1", (d) -> return d.source.y)
                      .attr("x2", (d) -> return d.target.x)
                      .attr("y2", (d) -> return d.target.y)

                  node.attr("cx", (d) -> return d.x)
                      .attr("cy", (d) -> return d.y)
              )
      #node = new Node()
      #console.log(node)
      #node.ping_node(0, null)
      #this.collection.add(node)

    addNode: (node) ->
      console.log("add")
      console.log(node)
      item = new NodeItem({model: node})
      this.$("ul").append(item.render().el)
    
    events:
      "keypress .js-kad-ping" : (e) ->
        key = e.keyCode || e.which
        $this = $(e.currentTarget)
        console.log($this)
        if key is 13 and $this.val() isnt ""
          console.log("if")
          this.collection.add(new Node())
          $this.val("")
          
      "keypress .js-kad-store" : (e) ->


      "keypress .js-kad-find-node" : (e) ->


      "keypress .js-kad-find-val" : (e) ->


      "keypress .js-kad-delete" : (e) ->


  class NodeItem extends Backbone.View
    initialize: ->
      console.log('init item')

    render: ->
      console.log("render item")
      console.log(this)
      return this

  network = new Network
  node0 = new Node(null)
  network.add(node0)
  network.add(new Node(node0)) for node in [0..19]
  #console.log("network: ")
  #console.log(network)
  #console.log("network JSON: " + JSON.stringify(network))
  #console.log("network links: ")
  #console.log(network.get_links())
  #console.log("network links JSON: " + JSON.stringify(network.get_links()))
  #network.test()
  #console.log(network.get_links())
  #console.log("network links JSON: " + JSON.stringify(network.get_links()))
  
  view = new NetworkView({collection: network})




