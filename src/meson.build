pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gnome_house')
gnome = import('gnome')

gnome.compile_resources('gnome_house',
  'gnome_house.gresource.xml',
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
  input: 'gnome_house.in',
  output: 'gnome_house',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gnome_house_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'libs/model.py',
  'libs/hueutilities.py',
  'libs/invenctory.py',
  'widgets/widgets.py'
]

install_data(gnome_house_sources, install_dir: moduledir)
