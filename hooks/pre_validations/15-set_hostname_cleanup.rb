unless app_value(:hostname).nil?
  hostname = app_value(:hostname)

  filename = '/etc/hosts'
  logger.debug("Cleaning temporary hostanme for loopback if set")
  unless kafo.noop?
    text = File.read(filename) 
    text.gsub!(/# temporary hostname for loopback\n127.0.0.1 #{hostname}\n/m, '')
    File.open(filename, "w") { |file| file.write(text) }
  end

  nil
end
