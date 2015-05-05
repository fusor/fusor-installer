unless app_value(:hostname).nil?
  hostname = app_value(:hostname)

  command = "hostname \"#{hostname}\" 2>&1"
  logger.debug(command)
  unless kafo.noop?
    result = `command`
    if $?.exitstatus > 0
      say "<%= color('Hostname setup failed: #{result}', :bad) %>"
      kafo.class.exit(101)
    end
  end

  filename = '/etc/sysconfig/network'
  logger.debug("Writing hostname (#{hostname}) to #{filename}")
  unless kafo.noop?
    entry = "HOSTNAME=#{hostname}"
    begin
      text = File.read(filename) 
      text.gsub!(/^HOSTNAME=.*?$/, entry)
      text += "#{entry}\n" unless text =~ /^HOSTNAME=/
      File.open(filename, "w") { |file| file.write(text) }
    rescue => error
      say "<%= color('Hostname setup failed: #{error}', :bad) %>"
      kafo.class.exit(101)
    end
  end
end
