import click
import requests

@click.group()
def cli():
    pass

@cli.command()
@click.option('--usuario', '-u', prompt=True, help='Usuario:')
@click.option('--contrasena','-p', prompt=True, hide_input=True, help='Contrasena:')
@click.option('--url', default='http://localhost:5000/api/Seguridad/login/', help='La URL del endpoint de autenticación')
def login(usuario, contrasena, url):
    response = requests.post(url, json={'usuario': usuario, 'contrasena': contrasena})

    if response.ok:
        data = response.json()
        if data['estado']:
            click.echo('Autenticación exitosa. Token generado: {}'.format(data['token']))
        else:
            click.echo('Error de autenticación: {}'.format(data['description']))
    else:
        click.echo('Error al conectarse al endpoint de autenticación')

if __name__ == '__main__':
    cli()
