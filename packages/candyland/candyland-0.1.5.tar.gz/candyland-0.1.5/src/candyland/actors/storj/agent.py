"""
    Appellation: pipeline
    Contributors: FL03 <jo3mccain@icloud.com> (https://gitlab.com/FL03)
    Description:
        ... Summary ...
"""
from candyland.components.pipelines import Sleeve, commands_from_dict


def storj_uri(bucket: str, *args):
    return "sj://" + "/".join([bucket, *args])


class Storj(object):
    def __init__(self):
        self.sleeve = Sleeve("uplink")

    def access(self, *args):
        return self.sleeve("access", *args)

    def cp(self, *args):
        return self.sleeve("cp", *args)

    def ls(self, *args):
        return self.sleeve("ls", *args)

    def mb(self, *args):
        return self.sleeve("mb", *args)

    def meta(self, *args):
        return self.sleeve("meta", *args)

    def mv(self, *args):
        return self.sleeve("mv", *args)

    def rb(self, *args):
        return self.sleeve("rb", *args)

    def rm(self, *args):
        return self.sleeve("rm", *args)

    def setup(self, *args):
        return self.sleeve("setup", *args)

    def share(self, *args):
        return self.sleeve("share", *args)

    def version(self):
        return self.sleeve("version")


class StorjExt(Storj):
    def static_website(self, dns: str, bucket: str, *args, **kwargs):
        return self.share(
            *["--dns", dns, storj_uri(bucket, *args), *commands_from_dict(**kwargs)]
        )


if __name__ == "__main__":
    agent = StorjExt()
    print(agent.version())
