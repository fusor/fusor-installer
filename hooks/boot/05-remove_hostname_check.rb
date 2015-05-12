# remove hostname check if it exists
check_file = File.join(KafoConfigure.root_dir, 'checks', 'hostname.rb')
hook_file = File.join(KafoConfigure.root_dir, 'hooks', 'pre', '10-check_hostname.rb')
begin
  File.delete(check_file)
  logger.info "The check #{check_file} was removed. It is replaced with the hook #{hook_file}"
rescue Exception
end
