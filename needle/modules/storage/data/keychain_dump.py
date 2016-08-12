from core.framework.module import BaseModule


class Module(BaseModule):
    meta = {
        'name': 'Keychain Dump',
        'author': '@LanciniMarco (@MWRLabs)',
        'description': 'Dump the keychain.',
        'options': (
            ('filter', False, False, 'Filter to apply when dumping the keychain. If empty, the entire keychain will be dumped'),
            ('output', True, False, 'Full path of the output file')
        ),
    }

    # ==================================================================================================================
    # UTILS
    # ==================================================================================================================
    def __init__(self, params):
        BaseModule.__init__(self, params)
        # Setting default output file
        self.options['output'] = self.local_op.build_temp_path_for_file(self, "keychain-dump.txt")
        # Setting default filter
        if self.APP_METADATA:
            self.printer.info('Setting filter to: %s (you can change it in options)' % self.APP_METADATA['binary_name'])
            self.options['filter'] = self.APP_METADATA['binary_name']

    # ==================================================================================================================
    # RUN
    # ==================================================================================================================
    def module_run(self):
        # Composing the command string
        cmd = '{}'.format(self.device.DEVICE_TOOLS['KEYCHAINDUMPER'])
        msg = "Dumping the keychain"
        if self.options['filter']:
            cmd += ' | grep "{}" -A 3 -B2'.format(self.options['filter'])
            msg += ' with filter: %s' % self.options['filter']
        # Dump Keychain
        self.printer.info(msg)
        out = self.device.remote_op.command_blocking(cmd)

        # Check output
        if out and filter(lambda x: "README" not in x, out):
            # Save to file
            outfile = self.options['output'] if self.options['output'] else None
            # Print to console
            self.print_cmd_output(out, outfile)
        else:
            if self.options['filter']:
                self.printer.warning('No content matches the filter. Ensure the screen is unlocked before dumping the keychain')
            else:
                self.printer.warning('No content found. Ensure the screen is unlocked before dumping the keychain')
