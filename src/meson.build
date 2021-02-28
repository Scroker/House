pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'lightcontroller')
gnome = import('gnome')

gnome.compile_resources('lightcontroller',
  'lightcontroller.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'lightcontroller.in',
  output: 'lightcontroller',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

lightcontroller_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'model.py',
  'widgets/group_view.py',
  'widgets/light_view.py',
  'widgets/bridge_view.py',
  'widgets/rename_row.py',
  'utilities.py'
]

install_data(lightcontroller_sources, install_dir: moduledir)
